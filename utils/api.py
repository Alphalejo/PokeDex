import streamlit as st

import requests
import utils.styles as styles

# Connect to the API
url = "https://pokeapi.co/api/v2/"

def get_data(asset="", name="", params=None):
    try:
        response = requests.get(f"{url}{asset}/{name}", params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def pokemon_data(asset="", asset_name=""):
    """
    Fetches data for all Pokemon.
    """
    data = get_data(asset, asset_name.lower())

    type_names = [type["type"]["name"] for type in data.get("types", [])]
    col1, col2 = st.columns([1,3])

    with col1:
        st.image(data["sprites"]["front_default"], use_container_width=True)
        st.markdown(f"<h3 style='text-align: center;'>#{data['id']}</h3>", unsafe_allow_html=True)
    
    with col2:
        st.header(f"{asset_name.capitalize()}")
        #____________________________________________________________________________________________________
        badges = "".join([styles.pokemon_type(type_name) for type_name in type_names])
        st.markdown(
            f"""
            <div style='display: flex; gap: 8px; flex-wrap: wrap;'>
                {badges}
            """,
            unsafe_allow_html=True
        )
      #______________________________________________________________________________________________________
        st.text(f"height: {data['height']}")
        st.text(f"weight: {data['weight']}")
        st.text(f"base experience: {data['base_experience']}")
