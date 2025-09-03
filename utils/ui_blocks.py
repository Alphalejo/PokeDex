import streamlit as st
import math


import utils.api as api
import utils.styles as styles
import utils.charts as charts
import utils.ML_algorithms as ML
import utils.chatbot as chatbot

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
        "Select Pokemons to compare:",
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

    if prediction == True:
        pokemon = pokemon1
    
    elif prediction == False:
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

def show_description(pokemon):
    description = api.get_pokemon_description(pokemon)

    # Sample data
    keys = list(description.keys())
    keys = [key.capitalize() for key in keys]
    page_size = 6
    num_pages = math.ceil(len(keys) / page_size)

    st.markdown("<div style='text-align: center;'><h3>Description on Each Generation</h3></div>", unsafe_allow_html=True)

    # Session state to track current page
    if "page" not in st.session_state:
        st.session_state.page = 1

    # Layout: arrows + tabs in one row
    nav_cols = st.columns([1, 15, 1])


    with nav_cols[0]:
        if st.button("◀", disabled=st.session_state.page == 1):
            st.session_state.page -= 1
            st.rerun()

    start = (st.session_state.page - 1) * page_size
    end = start + page_size
    tab_keys = keys[start:end]

    with nav_cols[1]:
        tabs = st.tabs(tab_keys)

    with nav_cols[2]:
        if st.button("▶", disabled=st.session_state.page == num_pages):
            st.session_state.page += 1
            st.rerun()

    # Tab content
    try:
        for tab, key in zip(tabs, tab_keys):
            with tab:
                st.markdown(description[key.lower()])
    except:
        st.write("No description available.")


#=======================================================================================================

def show_evolution_chain(pokemon):
    print(pokemon)
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
@st.fragment()
def chatbot_ui(pokemon):

    oak_avatar = "https://i.imgur.com/3vZSHwH.png"
    user_avatar = "https://i.imgur.com/h3kK4Cp.png"

    st.markdown("""
        <style>
                .st-emotion-cache-u4v75y{
                    max-height: 400px;
                    overflow-y: auto;
                     display: flex;
                    flex-direction: column-reverse;
                }
        </style>
    """, unsafe_allow_html=True)
    

    with st.container(border=True):
        if "history" not in st.session_state:
            st.session_state.history = []

        with st.chat_message("system", avatar=oak_avatar):
            st.write(f"Hey there, young trainer! I'm Professor Oak, and I've spent my life studying Pokémon. Do you want to know more about {pokemon}?")

        for message in st.session_state.history:
            with st.chat_message(message["role"], avatar=oak_avatar if message["role"] == "assistant" else user_avatar):
                st.write(message["content"])

        prompt = st.chat_input("Ask Professor Oak anything about Pokémon")

        if prompt:

            st.session_state.history.append({"role": "user", "content": prompt})

            #answer = chatbot.professor_oak(prompt, pokemon)
            answer = "Your mission is to educate, inspire, and support trainers in their journey through the Pokémon world."

            st.session_state.history.append({"role": "assistant", "content": answer})

            st.rerun()
    
    
    st.button("Clear", on_click=lambda: st.session_state.update({"history": []}))

# make chatbot collapsible to run only when necessary
def start_chat_ui(pokemon):

    if "enabled" not in st.session_state:
        st.session_state.enabled = False
    
    if st.session_state.enabled == False:
        if st.button("chat with oak", on_click=lambda: st.session_state.update({"enabled": True})):
            start_chat_ui(pokemon, enabled=True)
        

    if st.session_state.enabled == True:        
        with st.container(height=200, border=True):        
            chatbot_ui(pokemon)
            st.button("End Chat", on_click=lambda: st.session_state.update({"enabled": False}))
    
    st.session_state.enabled = False

