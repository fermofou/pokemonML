import requests
import json
import os
import shutil
from tqdm import tqdm
from PIL import Image

print("Starting Pokémon image processing...")

# --- Configuration ---
JSON_INPUT_FILE = "pokemon_data.json" # The file you already have
TEMP_PNG_DIR = "temp_png_images"
FINAL_WEBP_DIR = "pokemon_shiny_webp_images"

# --- Setup ---
# Create directories if they don't exist
os.makedirs(TEMP_PNG_DIR, exist_ok=True)
os.makedirs(FINAL_WEBP_DIR, exist_ok=True)

all_pokemon_data = {}

# --- Part 1: Load JSON and Download PNGs ---
try:
    with open(JSON_INPUT_FILE, "r") as f:
        all_pokemon_data = json.load(f)
    print(f"Successfully loaded '{JSON_INPUT_FILE}'.")
except FileNotFoundError:
    print(f"ERROR: '{JSON_INPUT_FILE}' not found. Please make sure it's in the same directory.")
    exit()
except json.JSONDecodeError:
    print(f"ERROR: Could not decode '{JSON_INPUT_FILE}'. The file may be corrupt.")
    exit()

print(f"Downloading {len(all_pokemon_data)} images to '{TEMP_PNG_DIR}'...")

# Loop through the loaded data
for pokemon_id, data in tqdm(all_pokemon_data.items(), desc="Downloading PNGs"):
    image_url_png = data.get('image_url')
    
    if not image_url_png:
        print(f"Warning: No 'image_url' found for Pokémon ID {pokemon_id}. Skipping.")
        continue

    # 4. Download the PNG image
    try:
        img_res = requests.get(image_url_png, stream=True)
        img_res.raise_for_status()
        # Save as {id}_shiny.png, e.g., "1_shiny.png"
        png_save_path = os.path.join(TEMP_PNG_DIR, f"{pokemon_id}_shiny.png")
        with open(png_save_path, 'wb') as f:
            shutil.copyfileobj(img_res.raw, f)
            
    except requests.exceptions.RequestException as img_e:
        print(f"Error downloading image for Pokémon ID {pokemon_id} ({image_url_png}): {img_e}")

print("All downloads finished.")

# --- Part 2: Convert PNGs to WebP ---
print(f"Converting images from '{TEMP_PNG_DIR}' to '{FINAL_WEBP_DIR}'...")

png_files = [f for f in os.listdir(TEMP_PNG_DIR) if f.endswith('.png')]

for filename in tqdm(png_files, desc="Converting to WebP"):
    try:
        png_path = os.path.join(TEMP_PNG_DIR, filename)
        # Filename without extension (e.g., "1")
        base_filename = os.path.splitext(filename)[0] 
        webp_path = os.path.join(FINAL_WEBP_DIR, f"{base_filename}.webp")
        
        # Open PNG and save as WebP
        with Image.open(png_path) as img:
            img.save(webp_path, 'WEBP', quality=85) # Adjust quality as needed
            
    except Exception as convert_e:
        print(f"Error converting {filename} to WebP: {convert_e}")

print("Conversion complete.")

# --- Part 3: Clean up temporary PNGs ---
try:
    shutil.rmtree(TEMP_PNG_DIR)
    print(f"Successfully deleted temporary directory: '{TEMP_PNG_DIR}'")
except OSError as e:
    print(f"Error deleting directory '{TEMP_PNG_DIR}': {e}")

print("\nImage processing finished.")
print(f"All WebP images are now in the '{FINAL_WEBP_DIR}' folder.")