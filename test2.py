import streamlit as st
import utils.api as api
import pandas as pd
import utils.ui_blocks as ui_blocks

def brief_pokemon_encounters(pokemon_encounters):
    raw_df = pd.DataFrame(pokemon_encounters)
    brief_df = raw_df.drop_duplicates(subset="pokemon").replace({pd.NA: None, pd.NaT: None, float('nan'): None})

    return brief_df["pokemon"].tolist(), brief_df["method"].tolist(), brief_df["chance"].tolist(), brief_df["max_level"].tolist(), brief_df["conditions"].tolist()

def pokemon_cards(pokemons, method = "walk", chance = 0, level = 0, condition = None):

    cols = st.columns(4)

    chunk_list = [pokemons[i:i + 4] for i in range(0, len(pokemons), 4)]
    counter = 0

    for chunk in chunk_list:
        for i in range(4):
            with cols[i]:
                try:
                    # Pokemon card ____________________________________________________________

                    if condition[i] == []:
                        condition[i] = "None"
                    with st.container(border=True):
                        st.image(api.get_pokemon_sprite(chunk[i]), use_container_width=True)
                        st.markdown(f"""<div style='text-align: center; font-size: 20px; font-weight: 600;'>
                                    {chunk[i].capitalize()}</div>""", unsafe_allow_html=True)
                        ui_blocks.show_pokemon_types(api.get_pokemon_types(chunk[i]))
                        st.markdown(f"""
                            <p><strong>Method:</strong> {method[counter]} </br>
                            <strong>Chance:</strong> {chance[i]}% </br>
                            <strong>Max Level:</strong> {level[i]}</br>
                            <strong>Conditions:</strong> {condition[i]}</p>
                            """, unsafe_allow_html=True)
                        
                        counter += 1
                    #___________________________________________________________________________
                except:
                    pass

def sub_area(sub_area):

    location_name, location_id, location_game_index, encounter_methods, pokemon_encounters = api.sub_area_data(sub_area)

    st.subheader(location_name.capitalize())
    st.markdown(f"<h6 style='padding-bottom: 0;'>🆔 ID: {location_id}  &emsp; 🎮 Game Index: {location_game_index}</h6>", unsafe_allow_html=True)

    st.divider()

    # show result
    st.markdown(f"""
        <h4 style='padding: 0;'>🚶 Encounter Methods:</h4>
        """, unsafe_allow_html=True)


    for method, versions in encounter_methods.items():
        st.markdown(f"<li style='margin-left: 50px;'><strong style='font-size: 20px;'>{method.capitalize()}:</strong> Encounter rate {versions[0]['rate']}%</li>", unsafe_allow_html=True)
        

    st.markdown(f"<h4></br>🔍 Pokémon Encounters:</h4>", unsafe_allow_html=True)
    
    # Show pokemon encounters
    pokemons, method, chance, level, condition = brief_pokemon_encounters(pokemon_encounters)
    pokemon_cards(pokemons, method, chance, level, condition)


#================================================================================================================    

def locations_ui(location):
    
    name, id, areas, generation, region = api.locations_data(location)

    st.markdown(f"<h2>{name}</h2>", unsafe_allow_html=True)


    if generation:
        st.markdown(f"<h5>🆔ID: {id} &emsp; 👾Generation: {generation.split('-')[-1].upper()}</h5>", unsafe_allow_html=True)
    
    if region:
        st.markdown(f"<h4>🗺️ Region: {region['name'].capitalize()}</h4>", unsafe_allow_html=True)


    if areas:
        st.markdown(f"<h4>Areas:</h4>", unsafe_allow_html=True)

        options = [area["name"] for area in areas]
        selected = st.radio("Select an area", options)

        for area in areas:
            if selected == area["name"]:
                with st.container(border=True):
                    sub_area(area["url"])
                

locations_ui("pallet-town")
