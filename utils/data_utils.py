import re
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def clean_text(data):
    cleaned = {}
    for version, text in data.items():
        # Remove control characters and soft hyphens
        text = text.replace('\x0c', ' ').replace('\xad', '')
        # Replace newlines with spaces
        text = text.replace('\n', ' ')
        # Normalize multiple spaces
        text = re.sub(r'\s+', ' ', text).strip()
        cleaned[version] = text
    return cleaned

#==============================================================================================

def brief_pokemon_encounters(pokemon_encounters):
    """
    Process raw Pokémon encounter data into a simplified structure.

    Args:
        pokemon_encounters (list[dict]): A list of dictionaries containing encounter details.

    Returns:
        tuple: Lists of Pokémon names, encounter methods, chances, max levels, and conditions.
    """

    logging.info("Converting encounters to DataFrame...")
    raw_df = pd.DataFrame(pokemon_encounters)

    logging.info(f"Initial DataFrame shape: {raw_df.shape}")

    # Drop duplicate encounters by Pokémon name
    brief_df = raw_df.drop_duplicates(subset="pokemon")
    logging.info(f"DataFrame shape after dropping duplicates: {brief_df.shape}")

    # Replace pandas-specific nulls with Python-native None
    brief_df = brief_df.replace({pd.NA: None, pd.NaT: None, float('nan'): None})
    logging.info("Replaced NaN and NA values with None.")

    # Extract lists from the DataFrame columns
    pokemon_list = brief_df["pokemon"].tolist()
    method_list = brief_df["method"].tolist()
    chance_list = brief_df["chance"].tolist()
    max_level_list = brief_df["max_level"].tolist()
    conditions_list = brief_df["conditions"].tolist()

    logging.info(f"Processed {len(pokemon_list)} unique encounters.")

    return pokemon_list, method_list, chance_list, max_level_list, conditions_list
