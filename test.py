"""import streamlit as st
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=[80, 90, 70, 60, 85, 80],
    theta=['Speed', 'Attack', 'Defense', 'HP', 'Special', 'Speed'],
    fill='toself',
    name='Pikachu',
    line=dict(color='gold'),
    fillcolor='rgba(255,215,0,0.3)'
))

fig.update_layout(
    polar=dict(bgcolor='rgba(0,0,0,0)'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)
"""

"""
import requests
import streamlit as st

url= "https://pokeapi.co/api/v2/pokemon?limit=100000"
response = requests.get(url).json()
pokemon_names = [entry['name'] for entry in response['results']]
print(len(pokemon_names))

st.multiselect(
    "Select Pokemon to compare:",
    options=pokemon_names)
"""
"""
import requests

data = requests.get("https://pokeapi.co/api/v2/pokemon/ditto").json()

try:
    pokemon_type = data['types'][1]['type']['name'] # Get the Pokémon's first type to know the color for the chart
except IndexError:
    pokemon_type = "other"
print(pokemon_type)
"""

"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

index= ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
cols = ['A', 'B', 'C', 'D']
df = pd.DataFrame(abs(np.random.randn(5, 4)), index=index, columns=cols)
df = df.style.background_gradient(cmap='YlOrRd')

st.dataframe(df, use_container_width=True)
"""

"""
import streamlit as st
import requests

url = "https://pokeapi.co/api/v2/type/"
name = "steel"
response = requests.get(f"{url}{name}").json()

st.header(f"id: {response['id']}")
st.title(f"name: {response['name']}")
st.text(f"damage_relations: {response['damage_relations']}")
#st.text(f"past_damage_relations: {response['past_damage_relations']}")
#st.text(f"game_indices: {response['game_indices']}")
#st.text(f"generation: {response['generation']}")
#st.text(f"move_damage_class: {response['move_damage_class']}")
#st.text(f"moves: {response['moves']}")
#st.text(f"pokemon: {response['pokemon']}")

st.header("Damage Relations")
st.text("double_damage_from:")
st.text([response['damage_relations']['double_damage_from'][i]['name'] for i in range(len(response['damage_relations']['double_damage_from']))])

st.text("double_damage_to:")
st.text([response['damage_relations']['double_damage_to'][i]['name'] for i in range(len(response['damage_relations']['double_damage_to']))])

st.text("half_damage_from:")
st.text([response['damage_relations']['half_damage_from'][i]['name'] for i in range(len(response['damage_relations']['half_damage_from']))])

st.text("half_damage_to:")
st.text([response['damage_relations']['half_damage_to'][i]['name'] for i in range(len(response['damage_relations']['half_damage_to']))])

st.text("No_damage_from:")
st.text([response['damage_relations']['no_damage_from'][i]['name'] for i in range(len(response['damage_relations']['no_damage_from']))])

st.text("no_damage_to:")
st.text([response['damage_relations']['no_damage_to'][i]['name'] for i in range(len(response['damage_relations']['no_damage_to']))])

import utils.api as api
import timeit

st.header("Damage Multipliers for Bulbasaur")
#st.text(api.get_damage_multipliers("bulbasaur")["attack"][0])
print(api.get_damage_multipliers("bulbasaur")["defence"])
#print(api.get_damage_multipliers("bulbasaur")["defence"].values())
#print([type for type, value in api.get_damage_multipliers("bulbasaur")['defence'].items() if value == 2])

print(api.get_damage_multipliers2("bulbasaur"))


time_a = timeit.timeit("api.get_damage_multipliers('bulbasaur')", globals=globals(), number=100)
time_b = timeit.timeit("api.get_damage_multipliers2('bulbasaur')", globals=globals(), number=100)

print(f"Function A took {time_a:.5f} seconds")
print(f"Function B took {time_b:.5f} seconds")
"""
"""
import utils.api as api

#print([api.get_data("pokemon","pikachu")["stats"][i]["base_stat"] for i in range(6)])
#print(api.get_data("pokemon-species","pikachu")["is_legendary"])

stats_pokemon1 = (
    [api.get_data("pokemon","pikachu")["stats"][i]["base_stat"] for i in range(6)]
)
api.get_data("pokemon-species","pikachu")["is_legendary"])
print(stats_pokemon1)
"""
"""
import utils.api as api

#print(np.full(17, False))
lista = [False] * 17
print(lista)

tipos = {
    'dark': 0, 'dragon': 1, 'electric': 2,
    'fairy': 3, 'fighting': 4, 'fire': 5,
    'flying': 6, 'ghost': 7, 'grass': 8,
    'ground': 9, 'ice': 10, 'normal': 11,
    'poison': 12, 'psychic': 13, 'rock': 14,
    'steel': 15, 'water': 16
}


pokemontypes = api.get_pokemon_types("bulbasaur")

for type in pokemontypes:
    lista[tipos[type]] = True

[lista[tipos[type]] = True for type in pokemontypes]
print(lista)
"""
"""
import utils.ui_blocks as blocks

print(blocks.predict_success("charizard", "blastoise"))
"""

"""import streamlit as st
import utils.api as api

pokemon = "venusaur"
data = api.get_data("pokemon", pokemon)
#st.title(f"{pokemon.capitalize()} Wins")
#st.image(data["sprites"]["front_default"], use_container_width=False, width=250)
#st.markdown(f"<h3 style='text-align: center;'>#{data['id']}</h3>", unsafe_allow_html=True)"""
#st.markdown(f"""
#    <div style='text-align: center;'>
#        <h1>{pokemon.capitalize()} Wins</h1>
#        <img src='{data["sprites"]["front_default"]}' width='250'/>
#        <h3>#{data['id']}</h3>
#    </div>
#""", unsafe_allow_html=True)



import streamlit as st
import utils.api as api

def loading():
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

loading()

pokemon = "venusaur"
data = api.get_data("pokemon", pokemon)
st.markdown(f"""
    <div style='text-align: center; position: relative; display: inline-block;'>
        <h1>{pokemon.capitalize()} Wins</h1>
        <img src='{data["sprites"]["front_default"]}' width='250' style='position: relative; z-index: 1;'/>
        <!-- GIF de celebración superpuesto -->
        <img src='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExODg0MWZydW1lMjJ3Zjd2YnM3cTU4ZXVqZXduNzd5eW5sbnY0YjQ0cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/gKrbnqo25MlI2TUC78/giphy.gif'
             style='position: absolute; top: 0; left: 50%; transform: translateX(-50%); z-index: 2; width: 300px;'/>
        <h3>#{data['id']}</h3>
    </div>
""", unsafe_allow_html=True)

import utils.ui_blocks as ui_blocks
import utils.charts as charts

class pokemondata:
    def __init__(self, asset, name):
        self.asset = asset
        self.name = name

    def display(self):
        ui_blocks.pokemon_data(self.asset, self.name)
        st.plotly_chart(charts.pokemon_stats_chart(asset=self.asset, name=self.name), use_container_width=True)


function = st.pills(
    label="Select Function",
    options=["Information", "Compare", "VS", "Team Generator"],
    selection_mode="single",
    default="Information",
)


with st.empty():
    if function == "Information":
        viewer = pokemondata("pokemon", "pikachu")
        viewer.display()

    elif function == "Compare":
        ui_blocks.pokemon_data("pokemon", "mew")
        st.plotly_chart(charts.pokemon_stats_chart(asset="pokemon", name="mew"), use_container_width=True)

    elif function == "VS":
        ui_blocks.pokemon_data("pokemon", "mewtwo")
        st.plotly_chart(charts.pokemon_stats_chart(asset="pokemon", name="mewtwo"), use_container_width=True)



if function == "Information":
        ui_blocks.pokemon_data("pokemon", "pikachu")
        st.plotly_chart(charts.pokemon_stats_chart(asset="pokemon", name="pikachu"), use_container_width=True)

elif function == "Compare":
        ui_blocks.pokemon_data("pokemon", "mew")
        st.plotly_chart(charts.pokemon_stats_chart(asset="pokemon", name="mew"), use_container_width=True)

elif function == "VS":
        ui_blocks.pokemon_data("pokemon", "mewtwo")
        st.plotly_chart(charts.pokemon_stats_chart(asset="pokemon", name="mewtwo"), use_container_width=True)