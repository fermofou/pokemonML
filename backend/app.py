from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from transformers import pipeline
from io import BytesIO
from PIL import Image
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, select, update, delete
import requests

# ---------------------- CONFIG ----------------------

DATABASE_URL = "postgresql+asyncpg://postgres:yourpassword@localhost:5432/yourdb"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

app = FastAPI()

# ---------------------- MODELS ----------------------

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    clerk_id = Column(String, unique=True, nullable=False)
    name = Column(String)
    photo_url = Column(String)

    cards = relationship("UserCard", back_populates="user")


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Numeric(10, 2))

    owners = relationship("UserCard", back_populates="card")


class UserCard(Base):
    __tablename__ = "user_cards"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"))
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="cards")
    card = relationship("Card", back_populates="owners")


# ---------------------- MODEL LOADING ----------------------

pipe = pipeline("object-detection", model="Matthieu68857/pokemon-cards-detection")

# ---------------------- STARTUP ----------------------

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ---------------------- HELPERS ----------------------

async def get_card_price(card_name: str):
    """Fetch card price from Pokémon TCG API"""
    try:
        resp = requests.get(f"https://api.pokemontcg.io/v2/cards?q=name:{card_name}")
        data = resp.json()
        if data.get("data"):
            market = data["data"][0].get("tcgplayer", {}).get("prices", {})
            price = (
                market.get("holofoil", {}).get("market")
                or market.get("normal", {}).get("market")
                or 0
            )
            return round(price or 0, 2)
        return 0
    except Exception as e:
        print("Error fetching price:", e)
        return 0


# ---------------------- ROUTES ----------------------

@app.post("/analyze")
async def analyze_card(user_clerk_id: str = Form(...), file: UploadFile = File(...)):
    """
    Detect card, fetch price, and add/update user card in DB.
    """
    image_bytes = await file.read()
    image = Image.open(BytesIO(image_bytes))
    results = pipe(image)

    if not results:
        raise HTTPException(status_code=400, detail="No card detected")

    card_label = results[0]["label"]
    confidence = results[0]["score"]
    price = await get_card_price(card_label)

    async with async_session() as session:
        # --- Ensure user exists ---
        user = (await session.execute(select(User).where(User.clerk_id == user_clerk_id))).scalar_one_or_none()
        if not user:
            user = User(clerk_id=user_clerk_id)
            session.add(user)
            await session.commit()

        # --- Ensure card exists ---
        card = (await session.execute(select(Card).where(Card.name == card_label))).scalar_one_or_none()
        if not card:
            card = Card(name=card_label, price=price)
            session.add(card)
            await session.commit()
        else:
            # Update price if changed
            card.price = price
            await session.commit()

        # --- Check if user already has this card ---
        user_card = (
            await session.execute(
                select(UserCard)
                .where(UserCard.user_id == user.id)
                .where(UserCard.card_id == card.id)
            )
        ).scalar_one_or_none()

        if user_card:
            user_card.quantity += 1
            action = "updated"
        else:
            session.add(UserCard(user_id=user.id, card_id=card.id, quantity=1))
            action = "added"

        await session.commit()

        return {
            "action": action,
            "user": user_clerk_id,
            "card": card_label,
            "price": price,
            "confidence": confidence
        }


@app.delete("/delete_card")
async def delete_card(user_clerk_id: str, card_name: str):
    """
    Delete a card from a user's collection.
    """
    async with async_session() as session:
        user = (await session.execute(select(User).where(User.clerk_id == user_clerk_id))).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        card = (await session.execute(select(Card).where(Card.name == card_name))).scalar_one_or_none()
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        user_card = (
            await session.execute(
                select(UserCard)
                .where(UserCard.user_id == user.id)
                .where(UserCard.card_id == card.id)
            )
        ).scalar_one_or_none()

        if not user_card:
            raise HTTPException(status_code=404, detail="User does not own this card")

        await session.delete(user_card)
        await session.commit()
        return {"message": f"Deleted {card_name} from user {user_clerk_id}"}


@app.get("/cards")
async def get_user_cards(user_clerk_id: str):
    """
    Get all cards owned by a user.
    """
    async with async_session() as session:
        user = (await session.execute(select(User).where(User.clerk_id == user_clerk_id))).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        result = await session.execute(
            select(Card.name, Card.price, UserCard.quantity)
            .join(UserCard, UserCard.card_id == Card.id)
            .where(UserCard.user_id == user.id)
        )

        cards = [{"name": r[0], "price": float(r[1]), "quantity": r[2]} for r in result.all()]
        return {"user": user_clerk_id, "cards": cards}
