import plotly.graph_objects as go
import random
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

import utils.api as api
import utils.styles as styles



def pokemon_stats_chart(asset="", name=""):
    """
    Fetches and displays a radar chart of Pokemon stats.
    """

    data = api.get_data(asset=asset, name=name)
    first_type = data['types'][0]['type']['name'] # Get the Pokémon's first type to know the color for the chart
    type_color = styles.types[first_type][0] if first_type in styles.types else "#FFFFFF"  # Default to white if type not found
    stats_names = [data['stats'][i]['stat']['name'].capitalize() for i in range(len(data['stats']))]
    stats_values = [data['stats'][i]['base_stat'] for i in range(len(data['stats']))]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=stats_values + [stats_values[0]],  # Close the radar chart
        theta=stats_names + [stats_names[0]],  # Close the radar chart
        fill='toself',
        name=name.capitalize(),
        line=dict(color=type_color),
        fillcolor=f'rgba({int(type_color[1:3], 16)},{int(type_color[3:5], 16)},{int(type_color[5:7], 16)},0.3)'  # Slightly transparent fill
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                #range=[0, 500],
                gridcolor="gray",
            ),
            bgcolor="rgba(0,0,0,0)"  # Transparent background for the radar chart
        ),
        font=dict(color="white"),
        showlegend=False
    )
    return fig

# =========================================================================================================================

def pokemon_multichart(pokemons_to_compare):
    """
    Fetches and displays a radar chart comparing multiple Pokemon stats.
    """
    fig = pokemon_stats_chart(asset="pokemon", name=pokemons_to_compare[0])
    data = api.get_data(asset="pokemon", name=pokemons_to_compare[0])
    pokemon_types = [data['types'][0]['type']['name']]

    for pokemon in pokemons_to_compare[1:]:

        # -----------------------------------------------------------------------------------------------------------------
        # Avoid having the same chart color for multiple Pokemons

        data = api.get_data(asset="pokemon", name=pokemon)
        pokemon_type = data['types'][0]['type']['name'] # Get the Pokémon's first type to know the color for the chart
        
        if pokemon_type in pokemon_types:
           # try:
            #    pokemon_type = data['types'][1]['type']['name']  # Get the Pokémon's second type if available
            #except IndexError:
            pokemon_type = random.choice(list(set(styles.types.keys()) - set(pokemon_types)))  # Fallback to a random type if no second type is available
        else:
            pass
        
        pokemon_types.append(pokemon_type)

        # ------------------------------------------------------------------------------------------------------------------

        type_color = styles.types[pokemon_type][0] if pokemon_type in styles.types else "#FFFFFF"  # Default to white if type not found
        stats_names = [data['stats'][i]['stat']['name'].capitalize() for i in range(len(data['stats']))]
        stats_values = [data['stats'][i]['base_stat'] for i in range(len(data['stats']))]

        fig.add_trace(go.Scatterpolar(
        r=stats_values + [stats_values[0]],  # Close the radar chart
        theta=stats_names + [stats_names[0]],  # Close the radar chart
        fill='toself',
        name= pokemon.capitalize(),
        line=dict(color=type_color),
        fillcolor=f'rgba({int(type_color[1:3], 16)},{int(type_color[3:5], 16)},{int(type_color[5:7], 16)},0.2)'  # Slightly transparent fill
            )
        )
        
        fig.update_layout(
            showlegend=True
        )

    return fig

#==========================================================================================================================

def pokemon_heatmap(pokemons_to_compare):
    """
    Fetches and displays a heatmap comparing multiple Pokemon stats.
    """

    df = pd.DataFrame(columns=["Pokemon", "HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"])
    
    for pokemon in pokemons_to_compare:
        data = api.get_data(asset="pokemon", name=pokemon)
        stats = {"Pokemon": pokemon.capitalize(),
                 "HP": data['stats'][0]['base_stat'],
                 "Attack": data['stats'][1]['base_stat'],
                 "Defense": data['stats'][2]['base_stat'],
                 "Special Attack": data['stats'][3]['base_stat'],
                 "Special Defense": data['stats'][4]['base_stat'],
                 "Speed": data['stats'][5]['base_stat']}
        new_row = pd.DataFrame([stats])
        df = pd.concat([df, new_row], ignore_index=True)

    df = df.style.background_gradient(
        cmap='OrRd',
        subset=df.columns[1:])

    return df