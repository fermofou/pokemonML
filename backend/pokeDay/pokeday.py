import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz  # For timezone-aware dates

# to run: .venv\Scripts\Activate.ps1 -> uvicorn pokeday:app --reload
# --- Configuration ---
JSON_FILE = "data_gen/pokemon_cleaned.json"
# Set the local timezone to get the correct "day"
LOCAL_TIMEZONE = pytz.timezone("America/Monterrey") 
# ---------------------

app = FastAPI(
    title="Pokémon of the Day API",
    description="Returns a specific Pokémon based on the day of the year.",
    version="1.0.0"
)

# --- CORS Middleware ---
# This allows your website (from any domain) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Data Store ---
# This dictionary will hold your JSON data in memory
pokemon_data_store = {}

# --- Helper Functions ---
def load_pokemon_data():
    """Loads the Pokémon JSON file into the global data store."""
    global pokemon_data_store
    if not os.path.exists(JSON_FILE):
        print(f"--- FATAL ERROR ---")
        print(f"'{JSON_FILE}' not found.")
        print("Please run the data generation and upload scripts first.")
        print("---------------------")
        # In a real app, you might want to exit, but for FastAPI,
        # we'll let it run and the endpoint will return an error.
        pokemon_data_store = {}
        return

    try:
        with open(JSON_FILE, "r") as f:
            pokemon_data_store = json.load(f)
        print(f"Successfully loaded {len(pokemon_data_store)} Pokémon from '{JSON_FILE}'.")
    except Exception as e:
        print(f"Error loading '{JSON_FILE}': {e}")
        pokemon_data_store = {}

def get_day_of_year_key() -> str:
    """
    Gets the current day of the year (1-366) as a string.
    Handles leap years.
    """
    # Get the current time in the specified timezone
    now = datetime.now(LOCAL_TIMEZONE)
    
    # .timetuple().tm_yday returns the day of the year (1-366)
    day_of_year = now.timetuple().tm_yday
    day_key = str(day_of_year)
    
    # --- Leap Year Logic ---
    # Your JSON only has 365 entries. If it's day 366 (Feb 29):
    # We'll check if "366" exists. If not, we'll serve Pokémon "1"
    # as a special fallback.
    if day_key == "366" and "366" not in pokemon_data_store:
        print("Leap day fallback: Serving Pokémon #1.")
        return "1"
        
    return day_key

# --- API Events ---
@app.on_event("startup")
def on_startup():
    """
    This function runs once when the FastAPI server starts.
    It loads the JSON data into memory.
    """
    print("Server starting up...")
    load_pokemon_data()

# --- API Endpoints ---
@app.get("/")
def read_root():
    """A simple root endpoint to show the API is running."""
    return {
        "message": "Pokémon of the Day API is running!",
        "docs": "/docs",
        "pokemon_endpoint": "/pokemon-of-the-day"
    }

@app.get("/today")
def get_pokemon_of_the_day():
    """
    Gets the Pokémon for the current day of the year.
    """
    if not pokemon_data_store:
        raise HTTPException(
            status_code=503, 
            detail=f"Service unavailable: Pokémon data file '{JSON_FILE}' is missing or empty."
        )
        
    # Get the key for today (e.g., "300")
    day_key = get_day_of_year_key()
    
    pokemon = pokemon_data_store.get(day_key)
    
    if not pokemon:
        raise HTTPException(
            status_code=404, 
            detail=f"No Pokémon data found for day {day_key}."
        )
    
    # Return the data for that Pokémon
    return {
        "day_of_year": int(day_key),
        **pokemon  # Unpacks the { name, color, types, normal_url, shiny_url }
    }

