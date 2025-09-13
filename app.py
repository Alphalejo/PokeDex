import streamlit as st

import utils.api as api
import utils.charts as charts
import utils.ui_blocks as ui_blocks

st.markdown("""
<style>
            .st-emotion-cache-1w723zb {
                padding-top: 2rem;
            }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
            <div style='text-align: center;'>
                <h1 style="font-size:5em; padding: 0;">UltraDex</h1>
                <i>More than a Pokédex — your AI battle partner</i>
                <br>
                <i><sub style="font-size: 0.8em; font-weight: normal;">By Alphalejo</sub></i>
            </div>""", unsafe_allow_html=True)



# -------------------------------------------------------------------

# CSS to make tabs occupy the full width
st.markdown("""
    <style>
    /* Make each tab take the same width */
    div[data-baseweb="tab-list"] > button {
        flex: 1;  /* Equal space for each tab */
        max-width: none !important;  /* Remove max-width restriction */
    }
    </style>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["PokeDex", "Pokemons Analysis", "Who Would Win?"])

# -------------------------------------------------------------------
with tab1:
    # Select asset type
    # take the selected option selected and convert it to lowercase
    asset = str(st.pills(
        label="Select Asset Type",
        options=["Pokemon", "Berry", "Item", "Location"],
        selection_mode="single",
        default="Pokemon",)
    ).lower()


    if asset == "pokemon":
        #input for asset name
        asset_name = str(st.selectbox(
            "Enter the name of a Pokemon:",
            options=api.all_items_names("pokemon"))
        )

    elif asset == "berry":
        #input for asset name
        asset_name = str(st.selectbox(
            "Enter the name of a Berry:",
            options=api.all_items_names("berry"))
        )

    elif asset == "item":
        #input for asset name
        asset_name = str(st.selectbox(
            "Enter the name of an Item:",
            options=api.all_items_names("item"))
        )
    
    elif asset == "location":
        #input for asset name
        asset_name = str(st.selectbox(
            "Enter the name of a region or zone:",
            options=api.all_items_names("location"))
        )

    if "asset_name" not in st.session_state:
        st.session_state.asset_name = []

    if asset_name != st.session_state.asset_name:
        st.session_state.asset_name = asset_name
        st.session_state.history = []

    # Display the Pokemon data
    if asset_name:
        #print(asset, asset_name) # Debugging line to check the asset and name
        
        if asset == "pokemon":
            
            cols = st.columns([1,3], vertical_alignment="center")

            with cols[0]:
                ui_blocks.pokemon_data(asset, asset_name)

            with cols[1]:
                with st.container():
                    ui_blocks.show_description(asset_name)

            
            with st.container():
                st.markdown("""
                    <style>
                        #tabs-bui2-tabpanel-0 > div > div:nth-child(4) > div > div > div > div.st-emotion-cache-u4v75y.eertqu02{
                            max-height: 400px;
                            overflow-y: auto;
                            display: flex;
                            flex-direction: column-reverse;
                        }
                    </style>
                """,unsafe_allow_html=True)
                ui_blocks.chatbot_ui(asset_name)

            st.markdown("""
                <div style='text-align: center;'>
                        <h2>Evolutions</h2>
                </div>
            """, unsafe_allow_html=True)
            try:
                ui_blocks.show_evolution_chain(asset_name)
            except:
                st.write("No evolution data available for this Pokémon.")

            try:    
                st.plotly_chart(charts.pokemon_stats_chart(asset=asset, name=asset_name), use_container_width=True)
            except:
                st.write("No stats available for this Pokémon.")

        elif asset == "berry":
            ui_blocks.berry_dashboard(asset_name)

        elif asset == "item":
            ui_blocks.items_visualization(asset_name)

        elif asset == "location":
            ui_blocks.locations_ui(asset_name)

        else:
            ui_blocks.not_found_icon()

with tab2:       
    ui_blocks.compare_dashboard()


with tab3:
# The function that compares and calculates the winner between two pokmemons
    
    st.write("VS Dashboard")

    col1, col2 = st.columns(2)

    # Select the first pokemon
    with col1:
        pokemon1 = st.selectbox(
            "Select the first Pokemon:",
            options=api.all_items_names("pokemon"),
            index=None,
            placeholder = "Select a Pokemon"
        )

        # Display the pokemon selected
        if pokemon1:
            left, center, right = st.columns([1,2,1])
            with center:
                ui_blocks.pokemon_data("pokemon", pokemon1)

    # Select the second pokemon
    with col2:
        pokemon2 = st.selectbox(
            "Select the second Pokemon:",
            options=api.all_items_names("pokemon"),
            index=None,
            placeholder = "Select a Pokemon"
        )

        # Display the pokemon selected
        if pokemon2: 
            left, center, right = st.columns([1,2,1])
            with center:
                ui_blocks.pokemon_data("pokemon", pokemon2)
    
    try:
        # Calculate the posible winner in a battle
        if pokemon1 and pokemon2:
            # Display the damage relations and strengths of both Pokemons
            ui_blocks.vs_dashboard(pokemon1, pokemon2)
            
            with st.empty():
                ui_blocks.loading_icon()
                success = ui_blocks.predict_success_block(pokemon1, pokemon2)
        else: pass
    
    except:
        # Center the icon
        st.markdown("<div style='display: flex; justify-content: center;'><img src='https://i.imgur.com/D0hhq7h.png' style='max-width: 300px;'></div>", unsafe_allow_html=True)

        # Center the message
        st.markdown(
            "<h4 style='text-align: center; font-weight: bold;'>One or both pokemons were not found, please try with different pokemons</h4>",
            unsafe_allow_html=True
        )
