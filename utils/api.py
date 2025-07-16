import streamlit as st

import requests
import utils.styles as styles
import utils.charts as charts

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
# Function to fetch data for all Pokemon names
# This function fetches data for all Pokemon and displays their names in a multiselect widget

def all_pokemon_names():

    response = requests.get(url+"pokemon?limit=20000").json()
    pokemon_names = [entry['name'] for entry in response['results']]
    
    return pokemon_names

#_____________________________________________________________________________________________________

def all_pokemon_types():
    """
    Fetches all Pokemon types.
    """
    response = requests.get(url + "type").json()
    return [type_info['name'] for type_info in response['results']]

#_____________________________________________________________________________________________________

def get_pokemon_sprite(pokemon_name):
    """
    Fetches the sprite URL for a given Pokemon name.
    """
    data = get_data(asset="pokemon", name=pokemon_name)
    if data and "sprites" in data and "front_default" in data["sprites"]:
        return data["sprites"]["front_default"]
    return None