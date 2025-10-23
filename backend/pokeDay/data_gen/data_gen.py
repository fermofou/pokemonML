import requests
import json
from tqdm import tqdm

print("Starting to fetch Pokémon data (1-365)...")

# Base URLs for PokeAPI
POKEMON_URL = "https://pokeapi.co/api/v2/pokemon/{}"
SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/{}"

all_pokemon_data = {}

# Loop from Pokémon ID 1 to 365
# tqdm adds a nice progress bar
for i in tqdm(range(1, 366), desc="Fetching Pokémon"):
    pokemon_data = {}
    try:
        # 1. Get primary data (name, types, sprites)
        res_pokemon = requests.get(POKEMON_URL.format(i))
        res_pokemon.raise_for_status() # Raises an error if the request failed
        data_pokemon = res_pokemon.json()
        
        # 2. Get species data (color)
        res_species = requests.get(SPECIES_URL.format(i))
        res_species.raise_for_status()
        data_species = res_species.json()
        
        # 3. Extract the specific fields we need
        name = data_pokemon['name'].capitalize()
        color = data_species['color']['name']
        
        # Get a list of all type names
        types = [t['type']['name'].capitalize() for t in data_pokemon['types']]
        
        # Get the high-quality official artwork URL
        # You can use this URL to download the images and put them in your own DB
        # The user's request mentioned a separate DB for webp, so this URL is what they'd use.
        image_url = data_pokemon['sprites']['other']['official-artwork']['front_default']
        
        if not image_url:
             # Fallback just in case official-artwork is missing
             image_url = data_pokemon['sprites']['front_default']

        # 4. Store it in our dictionary
        # We use the ID as the key (as a string, since JSON keys must be strings)
        all_pokemon_data[str(i)] = {
            "name": name,
            "color": color,
            "types": types,
            "image_url": image_url
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for Pokémon ID {i}: {e}")
        # Decide if you want to stop or continue
        # For this, we'll just skip this Pokémon
        continue

# 5. Write the complete dictionary to a JSON file
output_filename = "pokemon_data.json"
with open(output_filename, "w") as f:
    json.dump(all_pokemon_data, f, indent=2)

print(f"\nSuccessfully generated '{output_filename}' with {len(all_pokemon_data)} Pokémon.")
