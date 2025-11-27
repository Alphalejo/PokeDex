import streamlit as st
import math
import pandas as pd

import utils.api as api
import utils.styles as styles
import utils.charts as charts
import utils.ML_algorithms as ML
import utils.chatbot as chatbot
import utils.cache as cache
import utils.data_utils as data_utils


import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def show_pokemon_types(type_names):
    badges = "".join([styles.pokemon_type(type_name) for type_name in type_names])
    types = st.markdown(
        f"""
        <div style='display: flex; gap: 8px; flex-wrap: wrap; justify-content: center;'>
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

    try:
        st.image(data["sprites"]["front_default"], use_container_width=True)
    except:
        not_found_icon()
                
    st.markdown(
    """
    <style>
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True)

    st.markdown(f"""
                <div style='text-align: center;'><h3 style='text-align: center; padding: 0; margin-top: -30px;'>#{data['id']}</h3>
                <h3 style='padding: 0;'>{asset_name.capitalize()}</h3></div>
                """, unsafe_allow_html=True)
    
    show_pokemon_types(type_names)
    #____________________________________________________________________________________________________
    
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
            sprite_url = api.get_pokemon_sprite(pokemon, 96)
            st.markdown(
                f"""
                <div style='text-align:center;'>
                    <img src="{sprite_url}" style="max-height:220px; width:auto; max-width:96px;" />
                    <h4>{pokemon.capitalize()}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
    

#______________________________________________________________________________________________________________

def compare_dashboard():
    """
    Dashboard for comparing multiple Pokemon stats.
    """
    st.write("Compare Pokemon features")
    all_pokemons_to_compare = st.multiselect(
        "Select up to 5 Pokemons to compare:",
        options= api.all_items_names("pokemon"),
        max_selections=5
    )

    if all_pokemons_to_compare:

        show_selected_pokemons(all_pokemons_to_compare)

        st.dataframe(charts.pokemon_heatmap(all_pokemons_to_compare), use_container_width=True)
        
        #---------------------------------------------------------------
        #virifies that all pokemons are valid
        pokemons_to_compare = [] # Filtered data with valid pokemons

        for pokemon in all_pokemons_to_compare:
            data = api.get_data(asset="pokemon", name=pokemon)
            if data and "stats" in data:
                pokemons_to_compare.append(pokemon)
        #---------------------------------------------------------------


        if len(pokemons_to_compare) > 1:
            try:
                st.plotly_chart(charts.pokemon_multichart(pokemons_to_compare), use_container_width=True)
            except:
                st.write("No stats available for one or more of the selected Pokémons.")

    else:
        st.write("Please select at least two Pokemon to compare.")

#______________________________________________________________________________________________________________

def vs_dashboard(pokemon1, pokemon2):
    """
    Dashboard for comparing two Pokemon stats.
    """
    types1 = api.get_pokemon_types(pokemon1)
    types2 = api.get_pokemon_types(pokemon2)

    # Fetch damage relations for both Pokemons
    # Convert the damage relations to a more readable format (str instead of np.str_)
    strenghts1 = { key: [str(x) for x in value] for key, value in api.get_damage_relations(pokemon1).items()}
    strenghts2 = { key: [str(x) for x in value] for key, value in api.get_damage_relations(pokemon2).items()}

    col2_1, col2_2 = st.columns(2)

    with col2_1:
        #pokemon_data(asset="pokemon", asset_name=pokemon1)
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
        #pokemon_data(asset="pokemon", asset_name=pokemon2)
        #st.text(f"strenghts2: {', '.join(strenghts2['double_damage_to'])}")
        #st.text(f"Weakness2: {', '.join(strenghts2['double_damage_from'])}")

        if any(t in types1 for t in strenghts2["double_damage_from"]):
            st.badge(f"💀 {pokemon2} is weak against {pokemon1}", color="orange")
        
        elif any(t in types1 for t in strenghts2["double_damage_to"]):
            st.badge(f"⚔️ {pokemon2} is strong against {pokemon1}", color="green")
        
        elif any(t in types1 for t in strenghts2["no_damage_to"]):
            st.badge(f"❌ {pokemon2} has no effect to {pokemon1}", color="red")

        else: pass

#=======================================================================================================

def predict_success_block(pokemon1, pokemon2):

    prediction = ML.predict_success(pokemon1, pokemon2)

    if prediction[0] == True:
        pokemon = pokemon1
    
    elif prediction[0] == False:
        pokemon = pokemon2

    else:
        print("Unkown pokemon")

    data = api.get_data("pokemon", pokemon)
    st.markdown(f"""
        <div style='text-align: center;'>
            <h1>{pokemon.capitalize()} Wins</h1>
            <img src='{data["sprites"]["front_default"]}' width='250'/>
            <h3>#{data['id']}</h3>
            <!-- GIF de celebración superpuesto -->
        <img src='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExODg0MWZydW1lMjJ3Zjd2YnM3cTU4ZXVqZXduNzd5eW5sbnY0YjQ0cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/gKrbnqo25MlI2TUC78/giphy.gif'
             style='position: absolute; top: 0; left: 50%; transform: translateX(-50%); z-index: 2; width: 300px;'/>
        </div>""", unsafe_allow_html=True)
    

#=======================================================================================================

def loading_icon():
    
    lottie_html = """
            <h3 style="text-align: center; color: #FFF; padding-top: 50px;">Fighting...</h3>
                <div style="display: flex; justify-content: center; align-items: center;">
                    <script src="https://unpkg.com/@lottiefiles/dotlottie-wc@0.6.2/dist/dotlottie-wc.js" type="module"></script>
                    <dotlottie-wc 
                        src="https://lottie.host/9c3f548f-1f6b-4b43-bda7-78a72e2a0d0a/Nl7MBaCpvO.lottie"
                        style="width: 100px; height: 100px;" 
                        speed="1" autoplay loop>
                    </dotlottie-wc>
                </div>
            """

    return st.components.v1.html(lottie_html, height=400)


def not_found_icon(max_width=300):
    image_url = "https://i.imgur.com/D0hhq7h.png"

    return st.image(image_url, use_container_width=False, width=max_width)

#=======================================================================================================

@st.fragment
def show_description(name ,is_item = False, cols = 6):
    
    if is_item:
        description = cache.item_data_processed[name]["Descriptions"]

    else:
        description = api.get_pokemon_description(name)

    # Claves originales
    raw_keys = list(description.keys())
    page_size = cols
    num_pages = math.ceil(len(raw_keys) / page_size)

    st.markdown("<div style='text-align: center;'><h3>Description on Each Generation</h3></div>", unsafe_allow_html=True)

    # Estado de sesión
    if "page" not in st.session_state:
        st.session_state.page = 1

    # Layout de navegación
    nav_cols = st.columns([1, 15, 1])

    with nav_cols[0]:
        if st.button("◀", disabled=st.session_state.page == 1):
            st.session_state.page -= 1
            st.rerun()

    start = max(0, (st.session_state.page - 1) * page_size)
    end = min(len(raw_keys), start + page_size)

    # Claves para esta página
    page_keys = raw_keys[start:end]
    tab_labels = [key.capitalize() for key in page_keys]

    with nav_cols[1]:
        tabs = st.tabs(tab_labels)

    with nav_cols[2]:
        if st.button("▶", disabled=st.session_state.page == num_pages):
            st.session_state.page += 1
            st.rerun()

    # Contenido de las pestañas
    for tab, key in zip(tabs, page_keys):
        with tab:
            try:
                st.markdown(description[key])
            except KeyError:
                st.write("No description available.")



#=======================================================================================================
@st.fragment
def show_evolution_chain(pokemon):
    evolutions = api.get_evolution_chain(pokemon)

    number_cols = len(evolutions) + len(evolutions)-1
    columns = st.columns(number_cols)
    column = 0

    for evolution in evolutions:
        with columns[column]:
            try:
                sprite_url = api.get_pokemon_sprite(evolution)
                st.markdown(
                    f"""
                    <div style='text-align:center; overflow: visible;'>
                        <img src="{sprite_url}" style="max-height:220px; width:auto; max-width:96px;" />
                        <h4>{evolution.capitalize()}</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except:
                st.image("https://i.imgur.com/D0hhq7h.png", use_container_width=False)

        if column < number_cols-1:
            column += 1
            with columns[column]:
                st.markdown(
                    """
                    <div style='display: flex; justify-content: center; align-items: center; height: 100px;'>
                        <img src='https://i.imgur.com/sTF7vbT.png' style='height: 50px;'>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        else: break
        column += 1
    st.divider()

#=======================================================================================================

# Functions to run the AI chatbot with professor oak
# Create and build the chatbot

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@st.fragment()
def chatbot_ui(pokemon):
    """
    Streamlit UI for a chatbot that simulates Professor Oak,
    allowing the user to ask Pokémon-related questions.

    Args:
        pokemon (str): The Pokémon name currently in context.

    Returns:
        None. Renders the chatbot UI in Streamlit.
    """

    # Avatars for chat messages
    oak_avatar = "https://i.imgur.com/3vZSHwH.png"
    user_avatar = "https://i.imgur.com/h3kK4Cp.png"

    # Custom CSS for chat container (reverse scroll and auto height)
    st.markdown("""
        <style>
            #stVerticalBlockBorderWrapper {
                max-height: 400px;
                overflow-y: auto;
                display: flex;
                flex-direction: column-reverse;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        # Initialize session state
        if "history" not in st.session_state:
            st.session_state.history = []
            logging.info("Chat history initialized.")
        if "pending" not in st.session_state:
            st.session_state.pending = None
            logging.info("Pending state initialized.")

        # Intro message from Professor Oak
        with st.chat_message("system", avatar=oak_avatar):
            st.write(f"Hey there, young trainer! I'm Professor Oak, "
                     f"and I've spent my life studying Pokémon. "
                     f"Do you want to know more about {pokemon}?")

        # Render chat history
        for message in st.session_state.history:
            with st.chat_message(
                message["role"],
                avatar=oak_avatar if message["role"] == "assistant" else user_avatar
            ):
                st.write(message["content"])

        # Show "typing" indicator while waiting for response
        if st.session_state.pending:
            with st.chat_message("user", avatar=user_avatar):
                st.write(st.session_state.pending)

            with st.chat_message("system", avatar=oak_avatar):
                st.markdown(
                    """
                    <div style="display: flex; align-items: flex-start;">
                        <img src="https://i.imgur.com/QfGpyac.gif" 
                            alt="writing GIF" width="60" style="margin-top: -40px; margin-left: -20px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # User input box
        prompt = st.chat_input("Ask Professor Oak anything about Pokémon")

        if prompt:
            logging.info(f"User asked: {prompt}")
            # Add pending message
            st.session_state.pending = prompt
            st.rerun()

        # Process pending messages
        if st.session_state.pending:
            user_msg = st.session_state.pending
            st.session_state.history.append({"role": "user", "content": user_msg})

            # === Call the LLM (simulated here) ===
            logging.info("LLM response...")
            answer = chatbot.professor_oak(user_msg, pokemon)
            #answer = "Your mission is to educate, inspire, and support trainers in their journey through the Pokémon world."
            
            st.session_state.history.append({"role": "assistant", "content": answer})
            st.session_state.pending = None
            logging.info("Assistant response added to history.")
            st.rerun()

    # Clear history button
    st.button("Clear", on_click=lambda: st.session_state.update({"history": [], "pending": None}))


#=======================================================================================================

def berry_dashboard(asset_name):

    response = api.get_data("berry", asset_name)

    cols = st.columns([2,5])

    name = response['name'].capitalize()
    id = response['id']
    size = response['size']
    smoothness = response['smoothness']
    growth_time = response['growth_time']
    soil_dryness = response['soil_dryness']
    max_harvest = response['max_harvest']
    natural_gift_type = response['natural_gift_type']['name']
    natural_gift_power = response['natural_gift_power']

    with cols[0]:

        st.markdown(f"""
        <div style='text-align: left;'>
            <div style='display:flex;'><img style='object-fit: contain; width: 60px;' src='{api.berry_image(response)}'><h2>{name}</h2></div>
            <h3 style='padding:0'>ID: #{id}</h3>
            <p style='padding:0; margin-bottom: 0;'><b>Size:</b> {size}</p>
            <p style='padding:0; margin-bottom: 0;'><b>Smoothness:</b> {smoothness}</p>
            <p style='padding:0; margin-bottom: 0;'><b>Growth Time:</b> {growth_time} days</p>
            <p style='padding:0; margin-bottom: 0;'><b>Soil Dryness:</b> {soil_dryness}</p>
            <p style='padding:0; margin-bottom: 0;'><b>Max Harvest:</b> {max_harvest}</p>
            <p style='padding:0; margin-bottom: 0;'><b>Natural Gift Type:</b> {natural_gift_type}</p>
            <p style='padding:0; '><b>Natural Gift Power:</b> {natural_gift_power}</p>
        </div>
    """, unsafe_allow_html=True)

    with cols[1]:
        st.markdown("""
            <style>
                #tabs-bui2-tabpanel-0 > div > div.st-emotion-cache-13o7eu2.eertqu02 > div > div.stColumn.st-emotion-cache-1kf3zl5.eertqu01 > div > div.st-emotion-cache-13o7eu2.eertqu02 > div > div.st-emotion-cache-u4v75y.eertqu02{
                    max-height: 400px;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column-reverse;
                }
            </style>
        """,unsafe_allow_html=True)
        chatbot_ui(asset_name + " berry")


    #__________________________________________________________________________
    # Flavors
    flavors = response['flavors']

    flavor_names = [flavors[i]['flavor']['name'] for i in range(len(flavors))]
    flavor_potency = [flavors[i]['potency'] for i in range(len(flavors))]

    flavors_df = pd.DataFrame(flavor_potency, index=flavor_names).T

    st.subheader("Flavors")
    st.table(flavors_df)
    #__________________________________________________________________________


#=======================================================================================================

def items_visualization(name):
    """
    Visualizes item information in a Streamlit app.

    Args:
        name (str): The name of the Pokémon item.

    Returns:
        None. Displays the item data directly in the Streamlit UI.
    """
    try:
        logging.info(f"Fetching visualization data for item: {name}")

        # Get item data from API
        data = api.items_data(name)
        logging.debug(f"Item data retrieved for {name}: {data}")

        # Header with item image and name
        st.markdown(f"""
            <div style='display: flex; align-items: center;'>
                <img src='{data["image_url"]}' style='width: 60px; height: 60px;'>
                <h2>{name.capitalize()}</h2>
            </div>
            <p style='padding:0; margin-bottom: 0;'>{data["short_effect"]}</p>
            <p></p>
            """, unsafe_allow_html=True)

        # Create two columns for layout
        cols = st.columns([2, 5])
        with cols[0]:
            # Attributes section
            st.markdown("<p style='padding:0; margin-bottom: 0;'><h4>Attributes:</h4></p>", unsafe_allow_html=True)

            for attribute in data['attributes']:
                st.markdown(f"<li>{attribute.capitalize()}</li>", unsafe_allow_html=True)

            # Display basic stats
            data_to_show = ["baby_trigger_for", "category", "cost"]

            for stat in data_to_show:
                if data[stat]:
                    st.markdown(
                        f"<p><h4>{stat.capitalize()}: </h4>{data[stat]}</p>",
                        unsafe_allow_html=True
                    )

        with cols[1]:

            # Format the full effect text
            raw_text = data["effect"]
            formatted = raw_text.strip().replace('\n\n', '\n').replace('\n:', ':').replace('\n', '<br>')

            if data["effect"]:
                st.markdown(f"""<div style='display: flex; justify-content: center;'><h4>Effect</h4></div>
                            <div style='display: flex; text-align: center; justify-content: center; padding-bottom: 20px;'>
                                {formatted}
                            </div>""", unsafe_allow_html=True)

            # call the function to render the description UI
            show_description(name, is_item=True, cols=3)

        logging.info(f"Visualization for item {name} rendered successfully.")

    except Exception as e:
        logging.error(f"Error while visualizing item {name}: {e}", exc_info=True)
        st.subheader("Item not found")
    
    st.markdown("""
            <style>
                #tabs-bui2-tabpanel-0 > div > div:nth-child(6) > div > div.st-emotion-cache-u4v75y.eertqu02{
                    max-height: 400px;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column-reverse;
                }
            </style>
        """,unsafe_allow_html=True)
    chatbot_ui(name)


#=======================================================================================================

def pokemon_cards(pokemons, method="walk", chance=0, level=0, condition=None):
    """
    Render a grid of Pokémon cards in Streamlit.

    Args:
        pokemons (list[str]): List of Pokémon names.
        method (list[str] or str): Encounter method(s).
        chance (list[int] or int): Encounter chance(s).
        level (list[int] or int): Maximum level(s).
        condition (list or None): Encounter condition(s).
    """

    logging.info(f"Rendering cards for {len(pokemons)} Pokémon(s).")

    # Split the list of Pokémon into chunks of 4 for grid display
    chunk_list = [pokemons[i:i + 4] for i in range(0, len(pokemons), 4)]
    cols = st.columns(4)
    counter = 0

    for chunk in chunk_list:
        for i in range(4):
            try:
                pokemon_name = chunk[i]
                logging.debug(f"Rendering card for {pokemon_name}.")

                # Handle empty condition values
                if condition and condition[counter] == []:
                    condition[counter] = "None"

                # Card container
                with cols[i]:

                    st.markdown("""
                        <style>
                            #tabs-bui2-tabpanel-0 > div > div.st-emotion-cache-u4v75y.eertqu02{
                                width: 750px;
                                max-height: fit-content;
                            }
                        </style>""", unsafe_allow_html=True)

                    with st.container(border=True):
                        # Pokémon image
                        sprite = api.get_pokemon_sprite(pokemon_name)
                        st.image(sprite, use_container_width=True)

                        # Pokémon name
                        st.markdown(
                            f"""<div style='text-align: center; font-size: 20px; font-weight: 600;'>
                                {pokemon_name.capitalize()}</div>""",
                            unsafe_allow_html=True
                        )

                        # Pokémon types
                        types = api.get_pokemon_types(pokemon_name)
                        show_pokemon_types(types)

                        # Extra details
                        st.markdown(
                            f"""
                            <p style='font-size: 14px; margin-bottom: 0;'><strong>Method:</strong> {method[counter]} </br>
                            <strong>Chance:</strong> {chance[counter]}% </br>
                            <strong>Max Level:</strong> {level[counter]}</br>
                            <strong>Conditions:</strong><li style='font-size: 14px;'>{condition[counter]}</li></p>
                            """,
                            unsafe_allow_html=True
                        )

                        counter += 1

            except IndexError:
                pass
                #logging.warning("Attempted to access index out of range for one of the lists.")
            except Exception as e:
                logging.error(f"Error rendering card: {e}", exc_info=True)


#=======================================================================================================

def sub_area(sub_area):
    """
    Display details about a Pokémon sub-area including:
    - Location metadata
    - Encounter methods
    - Pokémon encounters

    Args:
        sub_area (str): Name or identifier of the sub-area.
    """

    logging.info(f"Fetching sub-area data for: {sub_area}")

    try:
        # Extract sub-area data
        location_name, location_id, location_game_index, encounter_methods, pokemon_encounters = api.sub_area_data(sub_area)
        logging.debug(f"Sub-area data retrieved for {sub_area}: "
                      f"location_name={location_name}, id={location_id}, game_index={location_game_index}")

        # Section: Location information
        st.subheader(location_name.capitalize())
        st.markdown(
            f"<h6 style='padding-bottom: 0;'>🆔 ID: {location_id}  &emsp; 🎮 Game Index: {location_game_index}</h6>",
            unsafe_allow_html=True
        )

        st.divider()

        # Section: Encounter methods
        st.markdown("<h4 style='padding: 0;'>🚶 Encounter Methods:</h4>", unsafe_allow_html=True)

        if encounter_methods:
            logging.info(f"Encounter methods found: {list(encounter_methods.keys())}")
            for method, versions in encounter_methods.items():
                try:
                    st.markdown(
                        f"<li style='margin-left: 50px;'><strong style='font-size: 18px;'>{method.capitalize()}:</strong> "
                        f"Encounter rate {versions[0]['rate']}%</li>",
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    logging.error(f"Error rendering encounter method {method}: {e}", exc_info=True)
        else:
            logging.warning(f"No encounter methods found for sub-area: {sub_area}")
            st.markdown("<p style='margin-left: 50px;'>No encounter methods available.</p>", unsafe_allow_html=True)

        # Section: Pokémon encounters
        st.markdown("<h4></br>🔍 Pokémon Encounters:</h4>", unsafe_allow_html=True)

        if pokemon_encounters:
            pokemons, method, chance, level, condition = data_utils.brief_pokemon_encounters(pokemon_encounters)
            logging.info(f"Rendering {len(pokemons)} Pokémon encounter(s) for {sub_area}")
            pokemon_cards(pokemons, method, chance, level, condition)
        else:
            logging.warning(f"No Pokémon encounters found for sub-area: {sub_area}")
            st.markdown("<p>No Pokémon encounters available.</p>", unsafe_allow_html=True)

    except Exception as e:
        logging.error(f"Failed to render sub-area {sub_area}: {e}", exc_info=True)
        st.error(f"⚠️ Could not load sub-area data for '{sub_area}'.")

#=======================================================================================================

def locations_ui(location: str):
    """
    Display location details including:
    - Name, ID, generation, and region
    - Sub-areas available in the location

    Args:
        location (str): The name or identifier of the location.
    """

    logging.info(f"Fetching location data for: {location}")

    st.markdown("""
            <style>
                #tabs-bui2-tabpanel-0 > div > div.st-emotion-cache-13o7eu2.eertqu02 > div > div.st-emotion-cache-u4v75y.eertqu02{
                    max-height: 400px;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column-reverse;
                }
            </style>
        """,unsafe_allow_html=True)

    chatbot_ui(location)

    try:
        # Retrieve data for the location
        name, id, areas, generation, region = api.locations_data(location)
        logging.debug(f"Location data: name={name}, id={id}, generation={generation}, region={region}")

        # Section: Location header
        st.markdown(f"<h2>{name}</h2>", unsafe_allow_html=True)

        if generation:
            st.markdown(
                f"<h5>🆔 ID: {id} &emsp; 👾 Generation: {generation.split('-')[-1].upper()}</h5>",
                unsafe_allow_html=True
            )
        else:
            logging.warning(f"No generation info for location: {location}")

        if region:
            st.markdown(f"<h4>🗺️ Region: {region['name'].capitalize()}</h4>", unsafe_allow_html=True)
        else:
            logging.warning(f"No region info for location: {location}")

        # Section: Areas
        if areas:
            st.markdown("<h4>Areas:</h4>", unsafe_allow_html=True)

            options = [area["name"] for area in areas]
            selected = st.radio("Select an area", options)

            # Render details for the selected area
            for area in areas:
                if selected == area["name"]:
                    try:
                        with st.container(border=True):
                            sub_area(area["url"])
                    except Exception as e:
                        logging.error(f"Failed to render sub-area {area['name']} ({area['url']}): {e}", exc_info=True)
                        st.error(f"⚠️ Could not load sub-area '{area['name']}'.")
        else:
            logging.warning(f"No areas found for location: {location}")
            st.markdown("<p>No areas available for this location.</p>", unsafe_allow_html=True)

    except Exception as e:
        logging.error(f"Failed to load location {location}: {e}", exc_info=True)
        st.error(f"⚠️ Could not load location data for '{location}'.")