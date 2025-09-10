import pandas as pd
import joblib
import logging

import utils.api as api
import utils.cache as cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG if you want more details
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_data(name1, name2):
    """
    Fetch Pokémon data for two Pokémon including stats, types, and legendary status.

    Args:
        name1 (str): Name of the first Pokémon.
        name2 (str): Name of the second Pokémon.

    Returns:
        tuple: (raw_data, types1, types2)
            - raw_data (list): Stats and legendary flags for both Pokémon.
            - types1 (list): Types of the first Pokémon.
            - types2 (list): Types of the second Pokémon.
    """

    logging.info(f"Fetching data for Pokémon: {name1} and {name2}")

    # Get Pokémon base data from the API
    data1 = api.get_data("pokemon", name1)
    data2 = api.get_data("pokemon", name2)
    logging.debug(f"Base data retrieved for {name1} and {name2}")

    # Get legendary flag from species endpoint (bypassing cache for accuracy)
    legendary1 = api.get_data("pokemon-species", name1, ignore_cache=True)["is_legendary"]
    legendary2 = api.get_data("pokemon-species", name2, ignore_cache=True)["is_legendary"]
    logging.debug(f"Legendary status - {name1}: {legendary1}, {name2}: {legendary2}")

    # Extract stats and append legendary flag
    stats1 = [data1['stats'][i]['base_stat'] for i in range(len(data1['stats']))] + [legendary1]
    stats2 = [data2['stats'][i]['base_stat'] for i in range(len(data2['stats']))] + [legendary2]
    logging.info(f"Stats extracted for {name1} and {name2}")

    # Get Pokémon types
    types1 = api.get_pokemon_types(name1)
    types2 = api.get_pokemon_types(name2)
    logging.info(f"Types retrieved - {name1}: {types1}, {name2}: {types2}")

    # Merge stats into raw_data (first Pokémon + second Pokémon)
    raw_data = stats1 + stats2
    logging.debug(f"Raw data combined: {raw_data}")

    logging.info("Data fetching and processing complete.")
    return raw_data, types1, types2

#____________________________________________________________________________________________________

def preprocess_data(raw_data, types1, types2):
    """
    Preprocess Pokémon data into a structured DataFrame for ML input.
    
    Args:
        raw_data (list): List of numerical stats and legendary flag for two Pokémon.
        types1 (list): List with primary and secondary type of Pokémon 1.
        types2 (list): List with primary and secondary type of Pokémon 2.
    
    Returns:
        DataFrame: A single-row DataFrame ready for ML prediction.
    """

    logging.info("Starting preprocessing of data for battle prediction.")

    # Define the base stat column names
    stats_names = ['HP_1', 'Attack_1', 'Defense_1', 'Sp. Atk_1', 'Sp. Def_1', 'Speed_1', 'Legendary_1', 
                  'HP_2', 'Attack_2', 'Defense_2', 'Sp. Atk_2', 'Sp. Def_2', 'Speed_2', 'Legendary_2']


    logging.debug(f"Raw column names generated: {stats_names}")

    # Map stats from raw_data into a dictionary
    stats_data = {}
    for i in range(len(stats_names)):
        stats_data[stats_names[i]] = raw_data[i]

    logging.info("Mapped raw stats into dictionary.")

    # Initialize dummy variables for Pokémon types (all start as 0)
    dummy_dict = {
        'Type 1_1_Dark': 0, 'Type 1_1_Dragon': 0, 'Type 1_1_Electric': 0, 'Type 1_1_Fairy': 0, 
        'Type 1_1_Fighting': 0, 'Type 1_1_Fire': 0, 'Type 1_1_Flying': 0, 'Type 1_1_Ghost': 0, 
        'Type 1_1_Grass': 0, 'Type 1_1_Ground': 0, 'Type 1_1_Ice': 0, 'Type 1_1_Normal': 0, 
        'Type 1_1_Poison': 0, 'Type 1_1_Psychic': 0, 'Type 1_1_Rock': 0, 'Type 1_1_Steel': 0, 
        'Type 1_1_Water': 0, 'Type 2_1_Dark': 0, 'Type 2_1_Dragon': 0, 'Type 2_1_Electric': 0, 
        'Type 2_1_Fairy': 0, 'Type 2_1_Fighting': 0, 'Type 2_1_Fire': 0, 'Type 2_1_Flying': 0, 
        'Type 2_1_Ghost': 0, 'Type 2_1_Grass': 0, 'Type 2_1_Ground': 0, 'Type 2_1_Ice': 0, 
        'Type 2_1_None': 0, 'Type 2_1_Normal': 0, 'Type 2_1_Poison': 0, 'Type 2_1_Psychic': 0, 
        'Type 2_1_Rock': 0, 'Type 2_1_Steel': 0, 'Type 2_1_Water': 0, 'Type 1_2_Dark': 0, 
        'Type 1_2_Dragon': 0, 'Type 1_2_Electric': 0, 'Type 1_2_Fairy': 0, 'Type 1_2_Fighting': 0, 
        'Type 1_2_Fire': 0, 'Type 1_2_Flying': 0, 'Type 1_2_Ghost': 0, 'Type 1_2_Grass': 0, 
        'Type 1_2_Ground': 0, 'Type 1_2_Ice': 0, 'Type 1_2_Normal': 0, 'Type 1_2_Poison': 0, 
        'Type 1_2_Psychic': 0, 'Type 1_2_Rock': 0, 'Type 1_2_Steel': 0, 'Type 1_2_Water': 0, 
        'Type 2_2_Dark': 0, 'Type 2_2_Dragon': 0, 'Type 2_2_Electric': 0, 'Type 2_2_Fairy': 0, 
        'Type 2_2_Fighting': 0, 'Type 2_2_Fire': 0, 'Type 2_2_Flying': 0, 'Type 2_2_Ghost': 0, 
        'Type 2_2_Grass': 0, 'Type 2_2_Ground': 0, 'Type 2_2_Ice': 0, 'Type 2_2_None': 0, 
        'Type 2_2_Normal': 0, 'Type 2_2_Poison': 0, 'Type 2_2_Psychic': 0, 'Type 2_2_Rock': 0, 
        'Type 2_2_Steel': 0, 'Type 2_2_Water': 0
    }

    logging.debug("Initialized dummy dictionary for Pokémon types.")

    # Build type keys dynamically from input
    type1_1 = f"Type 1_1_{types1[0].capitalize()}"
    type2_1 = f"Type 2_1_{types1[1].capitalize()}" if len(types1) > 1 and types1[1] else "Type 2_1_None"
    type1_2 = f"Type 1_2_{types2[0].capitalize()}"
    type2_2 = f"Type 2_2_{types2[1].capitalize()}" if len(types2) > 1 and types2[1] else "Type 2_2_None"


    for poke_type in [type1_1, type2_1, type1_2, type2_2]:
        if poke_type in dummy_dict:
            dummy_dict[poke_type] = 1
            logging.info(f"Set type {poke_type} to 1.")
        else:
            logging.warning(f"Type {poke_type} not found in dummy dictionary.")

    # Merge stats and dummy dict into one dictionary
    processed_data = stats_data | dummy_dict
    logging.info("Combined stats data with dummy dictionary.")

    # Convert dictionary into a DataFrame
    processed_df = pd.DataFrame([processed_data])  # Wrap dict in a list for single row DataFrame

    logging.info("Data preprocessing complete. Returning DataFrame.")

    return processed_df

#____________________________________________________________________________________________________


def predict_success(pokemon1, pokemon2):
    """
    Predict the outcome of a Pokémon battle between two Pokémon using a trained ML model.

    Args:
        pokemon1 (str): Name of the first Pokémon.
        pokemon2 (str): Name of the second Pokémon.

    Returns:
        tuple: (winner, probability)
            - winner (Bool): Model prediction, True if the pokemon 1 has more probability of win, otherwise it returns False.
            - probability (array): Prediction probabilities for each class.
    """

    logging.info(f"Starting prediction for battle: {pokemon1} vs {pokemon2}")

    # Load the trained ML model
    model_path = "./model/RandomForestClassifier.joblib"
    try:
        with open(model_path, "rb") as f:
            model = joblib.load(f)
        logging.info("Model loaded successfully.")
    except FileNotFoundError:
        logging.error(f"Model file not found at {model_path}")
        raise
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        raise

    # Get processed Pokémon data
    raw_data, types1, types2 = get_data(pokemon1, pokemon2)
    logging.debug(f"Raw data: {raw_data}, Types: {types1}, {types2}")

    # Check if processed data is already cached
    cache_key_1 = pokemon1 + pokemon2
    cache_key_2 = pokemon2 + pokemon1

    if cache_key_1 in cache.ML_data_input:
        data = cache.ML_data_input[cache_key_1]
        logging.info(f"Using cached data for {pokemon1} vs {pokemon2}")
    elif cache_key_2 in cache.ML_data_input:
        data = cache.ML_data_input[cache_key_2]
        logging.info(f"Using cached data for {pokemon2} vs {pokemon1}")
    else:
        data = preprocess_data(raw_data, types1, types2)
        cache.ML_data_input[cache_key_1] = data
        logging.info("Data preprocessed and cached.")

    # Perform prediction
    try:
        winner = model.predict(data)
        probability = model.predict_proba(data)
        logging.info(f"Prediction complete. Winner: {winner}, Probabilities: {probability}")
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise

    return winner, probability