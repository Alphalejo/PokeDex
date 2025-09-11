import streamlit as st
import utils.api as api

def locations_ui(location):

    data = api.get_data("location", name=location)

    st.session_state.sublocation = False
    
    try:
        name = next((place["name"] for place in data["names"] if place["language"]["name"] == "en"), location)
    except:
        name = location

    try:
        id = data["id"]
    except:
        id = ""

    try:
        areas = data["areas"]
    except:
        areas = False
    
    try:
        generation = data["game_indices"][0]["generation"]["name"]
    except:
        generation = False

    try:
        region = data["region"]
    except:
        region = False
    


    st.markdown(f"<h3>{name}</h3> <h4>ID: {id}</h4>", unsafe_allow_html=True)


    if generation:
        st.markdown(f"<h4>Generation: {generation.split('-')[-1].upper()}</h4>", unsafe_allow_html=True)
    
    if region:
        st.markdown(f"<h4>Region: {region['name'].capitalize()}</h4>", unsafe_allow_html=True)


    if areas:
        st.markdown(f"<h4>Areas:</h4>", unsafe_allow_html=True)

        for area in areas:
            button = st.button("⏩", key=area["name"])
            st.markdown(f"<li>{area['name']}: {button}</li>", unsafe_allow_html=True)
            
           # if st.button("⏩", key=area["name"]):
            #    st.session_state.sublocation = area["url"].split("/")[-2]



locations_ui("ruin-maniac-cave")