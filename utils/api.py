import requests
import numpy as np
import utils.data_utils as data_utils
from utils.cache import pokemon_data_cache

# Connect to the API
url = "https://pokeapi.co/api/v2/"

#_____________________________________________________________________________________________________
# Function to get data from the API
# This function fetches data for a specific asset and name, with optional parameters

def get_data(asset="", name="", params=None):
    
    if name in pokemon_data_cache.keys():
        return pokemon_data_cache[name]
    
    else:
        try:
            response = requests.get(f"{url}{asset}/{name}", params=params)
            response.raise_for_status()  # Raise an error for bad responses
            pokemon_data_cache[name] = response.json() # Cache the data for later use
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

#_____________________________________________________________________________________________________
# Function to fetch the types of a given Pokemon

def get_pokemon_types(pokemon_name):
    """
    Fetches the types of a given Pokemon.
    """
    data = get_data(asset="pokemon", name=pokemon_name)
    if data and "types" in data:
        return [type_info['type']['name'] for type_info in data['types']]
    return []

#_____________________________________________________________________________________________________
# Function to fetch data for all Pokemon names
# This function fetches data for all Pokemon and displays their names in a multiselect widget

def all_pokemon_names():

    response = requests.get(url+"pokemon?limit=20000").json()
    pokemon_names = [entry['name'] for entry in response['results']]
    
    return pokemon_names

#_____________________________________________________________________________________________________
# Function to fetch all Pokemon types

def all_pokemon_types():
    """
    Fetches all Pokemon types.
    """
    response = requests.get(url + "type").json()
    return [type_info['name'] for type_info in response['results']]

#_____________________________________________________________________________________________________
# Function to fetch the sprite URL for a given Pokemon name

def get_pokemon_sprite(pokemon_name):
    """
    Fetches the sprite URL for a given Pokemon name.
    """
    data = get_data(asset="pokemon", name=pokemon_name)
    if data and "sprites" in data and "front_default" in data["sprites"]:
        return data["sprites"]["front_default"]
    return None

#_____________________________________________________________________________________________________
# Function to display the pokedex description of each pokemon


# Pokémon API returns all descriptions for each game version and in multiple languages.
# In English, many are almost identical with only slight variations.

def get_pokemon_description(pokemon_name):

    pokemon_id = get_data(asset="pokemon-species", name=pokemon_name)["id"]

    # Pokémon API returns all descriptions for each game version and in multiple languages.
    # In English, many are almost identical with only slight variations.
    pokemon_data = get_data(asset="pokemon-species", name=pokemon_id)

    try:
        raw_descriptions = {entry["version"]["name"]: entry["flavor_text"] 
                    for entry in pokemon_data["flavor_text_entries"]
                    if entry["language"]["name"] == "en"}
    except Exception:
        raw_descriptions = "There's no description available for this Pokémon."

    # Text cleaning
    clean_description = data_utils.clean_texts(raw_descriptions)
    #unique_descriptions = data_utils.remove_similar_texts(list(clean_description))

    #full_description = "".join(unique_descriptions)
    return clean_description
#_____________________________________________________________________________________________________
# Function to fetch damage relations for a given Pokemon

def get_damage_multipliers(pokemon):
    """
    Fetches damage relations for a given Pokemon.
    """
    types = get_pokemon_types(pokemon)
    data = get_data(asset="type", name=types[0]) if types else None

    if types:
        #Create lists to store damage relations
        double_damage_from = [data['damage_relations']['double_damage_from'][i]['name'] for i in range(len(data['damage_relations']['double_damage_from']))]
        double_damage_to = [data['damage_relations']['double_damage_to'][i]['name'] for i in range(len(data['damage_relations']['double_damage_to']))]
        half_damage_from = [data['damage_relations']['half_damage_from'][i]['name'] for i in range(len(data['damage_relations']['half_damage_from']))]
        half_damage_to = [data['damage_relations']['half_damage_to'][i]['name'] for i in range(len(data['damage_relations']['half_damage_to']))]
        no_damage_from = [data['damage_relations']['no_damage_from'][i]['name'] for i in range(len(data['damage_relations']['no_damage_from']))]
        no_damage_to = [data['damage_relations']['no_damage_to'][i]['name'] for i in range(len(data['damage_relations']['no_damage_to']))]

        if len(types) > 1:
            # If the Pokemon has more than one type, fetch damage relations for the second type
            data = get_data(asset="type", name=types[1])
            double_damage_from += [data['damage_relations']['double_damage_from'][i]['name'] for i in range(len(data['damage_relations']['double_damage_from']))]
            double_damage_to += [data['damage_relations']['double_damage_to'][i]['name'] for i in range(len(data['damage_relations']['double_damage_to']))]
            half_damage_from += [data['damage_relations']['half_damage_from'][i]['name'] for i in range(len(data['damage_relations']['half_damage_from']))]
            half_damage_to += [data['damage_relations']['half_damage_to'][i]['name'] for i in range(len(data['damage_relations']['half_damage_to']))]
            no_damage_from += [data['damage_relations']['no_damage_from'][i]['name'] for i in range(len(data['damage_relations']['no_damage_from']))]
            no_damage_to += [data['damage_relations']['no_damage_to'][i]['name'] for i in range(len(data['damage_relations']['no_damage_to']))]

        else: pass
    else: return None

    types = np.array(all_pokemon_types())
    n_tipys = len(types)
    atack_relation = np.ones(n_tipys)  # Initialize attack relation with ones
    defence_relation = np.ones(n_tipys)  # Initialize defence relation with ones

    double_from_mask = np.isin(types, double_damage_from)
    double_to_mask = np.isin(types, double_damage_to)
    half_from_mask = np.isin(types, half_damage_from)
    half_to_mask = np.isin(types, half_damage_to)
    no_from_mask = np.isin(types, no_damage_from)
    no_to_mask = np.isin(types, no_damage_to)

    atack_relation[double_to_mask] *= 2
    atack_relation[half_to_mask] *= 0.5
    atack_relation[no_to_mask] *= 0

    defence_relation[double_from_mask] *= 2
    defence_relation[half_from_mask] *= 0.5
    defence_relation[no_from_mask] *= 0

    return [types, atack_relation, defence_relation]

#_____________________________________________________________________________________________________
# Function to calculate damage multipliers for a given Pokemon

def get_damage_relations(pokemon):
    
    damage_multipliers = get_damage_multipliers(pokemon)

    double_damage_from = []
    double_damage_to = []
    half_damage_from = []
    half_damage_to = []
    no_damage_from = []
    no_damage_to = []

    for type, attack, deffence in zip(damage_multipliers[0], damage_multipliers[1], damage_multipliers[2]):
        if attack == 2:
            double_damage_to.append(type)
        elif attack == 0.5:
            half_damage_to.append(type)
        elif attack == 0:
            no_damage_to.append(type)
        else: pass

        if deffence == 2:
            double_damage_from.append(type)
        elif deffence == 0.5:
            half_damage_from.append(type)
        elif deffence == 0:
            no_damage_from.append(type)
        else: pass

    return {
        "double_damage_from": double_damage_from,
        "double_damage_to": double_damage_to,
        "half_damage_from": half_damage_from,
        "half_damage_to": half_damage_to,
        "no_damage_from": no_damage_from,
        "no_damage_to": no_damage_to}

#_____________________________________________________________________________________________________
 
def get_evolution_chain(pokemon_name):
    """Fetches the evolution chain for a given Pokémon name."""
    # 1. Get species info
    species = get_data("pokemon-species", pokemon_name)
    evo_url = species["evolution_chain"]["url"]

    # 2. Get evolution chain
    evo_chain = requests.get(evo_url).json()
    current = evo_chain["chain"]

    evolutions = []

    while current:
        evolutions.append(current["species"]["name"])
        current = current["evolves_to"][0] if current["evolves_to"] else None

    return evolutions


print(get_evolution_chain("pikachu"))
