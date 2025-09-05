import requests
import utils.data_utils as data_utils
import utils.api as api
import streamlit as st

url = "https://pokeapi.co/api/v2/"


def items_data(name):

    asset = "item"
    response = api.get_data(asset, name)

    attributes = [response['attributes'][i]['name'] for i in range(len(response['attributes']))]
    baby_trigger_for = response['baby_trigger_for']
    category = response['category']
    cost = response['cost']

    effect = response['effect_entries'][0]['effect']
    short_effect = response['effect_entries'][0]['short_effect']

    image = response['sprites']['default']

    descriptions = {entry['version_group']['name']: entry['text']
                    for entry in response['flavor_text_entries']
                    if entry['language']['name'] == 'en'}

    clean_descriptions = data_utils.clean_texts(descriptions)

    all_data = {
        "attributes": attributes,
        "baby_trigger_for": baby_trigger_for,
        "category": category,
        "cost": cost,
        "effect": effect,
        "short_effect": short_effect,
        "image_url": image,
        "Descriptions": clean_descriptions
    }

    return (all_data)

def items_visualization(name):

    data = items_data(name)

    cols = st.columns([1,3])

    with cols[0]:
        st.markdown("""
            data["image_url"]
                    """)

name="master-ball"

items_visualization(name)

