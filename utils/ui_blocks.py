import streamlit as st
import pandas as pd
import numpy as np

import utils.api as api
import utils.styles as styles
import utils.charts as charts

import joblib



def show_pokemon_types(type_names):
    badges = "".join([styles.pokemon_type(type_name) for type_name in type_names])
    types = st.markdown(
        f"""
        <div style='display: flex; gap: 8px; flex-wrap: wrap;'>
            {badges}
        """,
        unsafe_allow_html=True
    )
    return types

#=========================================================================================================================

# Function to fetch data for all Pokemon
# This function fetches data for all Pokemon and displays their names in a multiselect widget
def pokemon_data(asset="", asset_name=""):
    """
    Fetches data for all Pokemon.
    """
    data = api.get_data(asset, asset_name)

    type_names = api.get_pokemon_types(asset_name)
    col1, col2 = st.columns([1,3])

    with col1:
        st.image(data["sprites"]["front_default"], use_container_width=True)
        st.markdown(f"<h3 style='text-align: center;'>#{data['id']}</h3>", unsafe_allow_html=True)
    
    with col2:
        st.header(f"{asset_name.capitalize()}")
        #____________________________________________________________________________________________________
        show_pokemon_types(type_names)
      #______________________________________________________________________________________________________
    

#=========================================================================================================================
# Function to display the compare dashboard

def show_selected_pokemons(pokemons_to_compare):
    """
    Displays the selected Pokemons in a grid format with a maximum image height.
    """
    cols = st.columns(len(pokemons_to_compare))

    for i, pokemon in enumerate(pokemons_to_compare):
        with cols[i]:
            sprite_url = api.get_pokemon_sprite(pokemon)
            st.markdown(
                f"""
                <div style='text-align:center;'>
                    <img src="{sprite_url}" style="max-height:220px; width:auto;" />
                    <h4>{pokemon.capitalize()}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

#______________________________________________________________________________________________________________

    

#______________________________________________________________________________________________________________

def compare_dashboard():
    """
    Dashboard for comparing multiple Pokemon stats.
    """
    st.write("Compare Pokemon features")
    pokemons_to_compare = st.multiselect(
        "Select Pokemons to compare:",
        options= api.all_pokemon_names(),
        max_selections=5
    )

    if pokemons_to_compare:

        show_selected_pokemons(pokemons_to_compare)

        st.dataframe(charts.pokemon_heatmap(pokemons_to_compare), use_container_width=True)

        st.plotly_chart(charts.pokemon_multichart(pokemons_to_compare), use_container_width=True)

    else:
        st.write("Please select at least one Pokemon to compare.")

#______________________________________________________________________________________________________________

def vs_dashboard(pokemon1, pokemon2):
    """
    Dashboard for comparing two Pokemon stats.
    """
    if pokemon1 and pokemon2:

        types1 = api.get_pokemon_types(pokemon1)
        types2 = api.get_pokemon_types(pokemon2)

        # Fetch damage relations for both Pokemons
        # Convert the damage relations to a more readable format (str instead of np.str_)
        strenghts1 = { key: [str(x) for x in value] for key, value in api.get_damage_relations(pokemon1).items()}
        strenghts2 = { key: [str(x) for x in value] for key, value in api.get_damage_relations(pokemon2).items()}

        col2_1, col2_2 = st.columns(2)

        with col2_1:
            pokemon_data(asset="pokemon", asset_name=pokemon1)
            #st.text(f"strenghts1: {strenghts1['double_damage_from']}")
            #st.text(f"Weakness1: {', '.join(strenghts1['double_damage_from'])}")

            if any(t in types2 for t in strenghts1["double_damage_from"]):
                st.badge(f"💀 {pokemon1} is weak against {pokemon2}", color="orange")
            
            elif any(t in types2 for t in strenghts1["double_damage_to"]):
                st.badge(f"⚔️ {pokemon1} is strong against {pokemon2}", color="green")

            elif any(t in types2 for t in strenghts1["no_damage_to"]):
                st.badge(f"❌ {pokemon1} has no effect to {pokemon2}", color="red")

            else: pass

        with col2_2:
            pokemon_data(asset="pokemon", asset_name=pokemon2)
            #st.text(f"strenghts2: {', '.join(strenghts2['double_damage_to'])}")
            #st.text(f"Weakness2: {', '.join(strenghts2['double_damage_from'])}")

            if any(t in types1 for t in strenghts2["double_damage_from"]):
                st.badge(f"💀 {pokemon2} is weak against {pokemon1}", color="orange")
            
            elif any(t in types1 for t in strenghts2["double_damage_to"]):
                st.badge(f"⚔️ {pokemon2} is strong against {pokemon1}", color="green")
            
            elif any(t in types1 for t in strenghts2["no_damage_to"]):
                st.badge(f"❌ {pokemon2} has no effect to {pokemon1}", color="red")

            else: pass

    else:
        st.write("Please select both Pokemons to compare.")

#=======================================================================================================

def predict_success(pokemon1, pokemon2):

    model = joblib.load("C:\Projects\PokeDex\model\RandomForestClassifier.joblib")

    stats_pokemon1 =(
        [api.get_data("pokemon",pokemon1)["stats"][i]["base_stat"] for i in range(6)]
    )
    stats_pokemon1.append(api.get_data("pokemon-species",pokemon1)["is_legendary"])

    stats_pokemon2 =(
        [api.get_data("pokemon",pokemon2)["stats"][i]["base_stat"] for i in range(6)]
    )
    stats_pokemon2.append(api.get_data("pokemon-species",pokemon2)["is_legendary"])

    # The model recives a boolean list for the pokemon type
    pokemon1_type1 = [False] * 17
    pokemon1_type2 = [False] * 17
    # The type number 18 is none, when the pokemon has only one type
    pokemon2_type1 = [False] * 18
    pokemon2_type2 = [False] * 18

    # Index of each type in the boolean list
    types1 = {
    'dark': 0, 'dragon': 1, 'electric': 2,
    'fairy': 3, 'fighting': 4, 'fire': 5,
    'flying': 6, 'ghost': 7, 'grass': 8,
    'ground': 9, 'ice': 10, 'normal': 11,
    'poison': 12, 'psychic': 13, 'rock': 14,
    'steel': 15, 'water': 16}

    types2 = {
    'dark': 0, 'dragon': 1, 'electric': 2,
    'fairy': 3, 'fighting': 4, 'fire': 5,
    'flying': 6, 'ghost': 7, 'grass': 8,
    'ground': 9, 'ice': 10, 'none' : 11, 'normal': 12,
    'poison': 13, 'psychic': 14, 'rock': 15,
    'steel': 16, 'water': 17}

    # Replacing false for True the pokemon types
    pokemon1_type1[types1[api.get_pokemon_types(pokemon1)[0]]] = True
    try:
        pokemon1_type2[types2[api.get_pokemon_types(pokemon1)[1]]] = True
    except:
        pokemon1_type2[types2['none']] = True

    pokemon2_type1[types1[api.get_pokemon_types(pokemon2)[0]]] = True
    try:
        pokemon2_type2[types2[api.get_pokemon_types(pokemon2)[1]]] = True
    except:
        pokemon2_type2[types2['none']] = True

    # Generate the final list to feed the ML algorithm
    total_stats = stats_pokemon1 + stats_pokemon2 + pokemon1_type1 + pokemon2_type1 + pokemon1_type2 + pokemon2_type2
    
    return model.predict(np.array(total_stats).reshape(1,-1))
     