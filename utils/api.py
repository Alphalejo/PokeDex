import requests

# Connect to the API
url = "https://pokeapi.co/api/v2/"

#_____________________________________________________________________________________________________
# Function to get data from the API
# This function fetches data for a specific asset and name, with optional parameters

def get_data(asset="", name="", params=None):
    try:
        response = requests.get(f"{url}{asset}/{name}", params=params)
        response.raise_for_status()  # Raise an error for bad responses
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

    #-------------------------------------------------------------
    # Create dictionaries to store attack and defence relations (damage multipliers)
    atack_relation = dict.fromkeys(all_pokemon_types(), 1)   

    for type_name in list(set(double_damage_to)):
        atack_relation[type_name] *= 2
    
    for type_name in list(set(half_damage_to)):
        atack_relation[type_name] *= 0.5
    
    for type_name in list(set(no_damage_to)):
        atack_relation[type_name] *= 0

    #------------------------------------------------------------
    defence_relation = dict.fromkeys(all_pokemon_types(), 1)

    for type_name in list(set(double_damage_from)):
        defence_relation[type_name] *= 2

    for type_name in list(set(half_damage_from)):
        defence_relation[type_name] *= 0.5

    for type_name in list(set(no_damage_from)):
        defence_relation[type_name] *= 0

    return {
        "attack": atack_relation,
        "defence": defence_relation
    }

#_____________________________________________________________________________________________________
# Function to calculate damage multipliers for a given Pokemon

def get_damage_relations(pokemon):
    
    damage_multipliers = get_damage_multipliers(pokemon)

    double_damage_from = damage_multipliers['defence']['double_damage_from']
    double_damage_to
    return {
        "double_damage_from": double_damage_from,
        "double_damage_to": double_damage_to,
        "half_damage_from": half_damage_from,
        "half_damage_to": half_damage_to,
        "no_damage_from": no_damage_from,
        "no_damage_to": no_damage_to}

#_____________________________________________________________________________________________________
 