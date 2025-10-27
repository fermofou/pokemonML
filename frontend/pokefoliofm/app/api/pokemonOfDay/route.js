// app/api/pokemonOfDay/route.js
export async function GET() {
  try {
    const res = await fetch("http://localhost:8000/today");

    if (!res.ok) {
      throw new Error("Failed to fetch Pokemon");
    }

    const data = await res.json();
    return Response.json(data);
  } catch (error) {
    return Response.json(
      { error: "Failed to fetch Pokemon of the day" },
      { status: 500 }
    );
  }
}
