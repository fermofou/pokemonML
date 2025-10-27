// src/lib/utils/getPokemonOfDay.ts
export interface Pokemon {
  day_of_year: number;
  name: string;
  color: string;
  types: string[];
  normal_url: string;
  shiny_url: string;
}

export async function getPokemonOfDay(): Promise<Pokemon> {
  const baseUrl =
    process.env.NODE_ENV === "production"
      ? "https://your-domain.com"
      : "http://localhost:3000";

  const res = await fetch(`${baseUrl}/api/pokemonOfDay`);
  if (!res.ok) throw new Error("Failed to fetch Pokémon");
  return res.json();
}
