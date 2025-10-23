import json

def remove_image_urls(input_file, output_file):
    # Load JSON data
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Iterate over each Pokémon entry
    for key, value in data.items():
        # Delete all keys that end with '_url'
        keys_to_delete = [k for k in value.keys() if k.startswith("image_url")]
        for k in keys_to_delete:
            del value[k]

    # Save cleaned data
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Removed image URLs. Saved cleaned data to '{output_file}'.")


if __name__ == "__main__":
    remove_image_urls("pokemon_data.json", "pokemon_cleaned.json")
