import requests
import json
import os
from tqdm import tqdm

print("Starting to update URLs to shiny versions...")

# --- Configuration ---
JSON_FILE = "pokemon_data.json" # The file you already have
POKEMON_URL = "https://pokeapi.co/api/v2/pokemon/{}"

# --- Part 1: Load Existing JSON ---
all_pokemon_data = {}
if not os.path.exists(JSON_FILE):
    print(f"ERROR: '{JSON_FILE}' not found. Please create it first.")
    exit()

try:
    with open(JSON_FILE, "r") as f:
        all_pokemon_data = json.load(f)
    print(f"Successfully loaded '{JSON_FILE}'.")
except json.JSONDecodeError:
    print(f"ERROR: Could not decode '{JSON_FILE}'. The file may be corrupt.")
    exit()

print(f"Fetching shiny URLs for {len(all_pokemon_data)} Pokémon...")

# --- Part 2: Loop, Fetch Shiny URL, and Update Data ---

# We loop using the keys from the loaded JSON file
for pokemon_id in tqdm(all_pokemon_data.keys(), desc="Fetching shiny URLs"):
    try:
        # 1. Make one API call to get sprite data
        res_pokemon = requests.get(POKEMON_URL.format(pokemon_id))
        res_pokemon.raise_for_status()
        data_pokemon = res_pokemon.json()
        
        # 2. Get the high-quality SHINY artwork URL
        shiny_url = data_pokemon['sprites']['other']['official-artwork']['front_shiny']
        
        if not shiny_url:
             # Fallback just in case official-artwork is missing
             shiny_url = data_pokemon['sprites']['front_shiny']
             
        if not shiny_url:
            print(f"Warning: No shiny URL found for Pokémon ID {pokemon_id}. Skipping update.")
            continue

        # 3. Update the URL in our dictionary
        all_pokemon_data[pokemon_id]["image_url"] = shiny_url
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for Pokémon ID {pokemon_id}: {e}")
        continue

# --- Part 3: Write the updated dictionary back to the JSON file ---
try:
    with open(JSON_FILE, "w") as f:
        json.dump(all_pokemon_data, f, indent=2)
    print(f"\nSuccessfully updated '{JSON_FILE}' with shiny image URLs.")
except IOError as e:
    print(f"Error writing to file '{JSON_FILE}': {e}")

print("Update process finished.")
