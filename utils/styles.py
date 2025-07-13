import streamlit as st

def Pokemon_type_style (bg_color, font_color, type_name):
    """
    Returns a styled HTML span element for the given Pokemon type.
    """
    return (f"""
        <span style='
            background-color: {bg_color};
            color: {font_color};
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 500;
        '>{type_name}</span>
        """)
 
def pokemon_type(type_name):
    types = {
        "normal": Pokemon_type_style ("#c996a5", "#6f525a", "Normal"),
        "fire": Pokemon_type_style ("#ae1d26", "#FD4B5A", "Fire"),
        "water": Pokemon_type_style ("#1552E1", "#85A8FB", "Water"),
        "grass": Pokemon_type_style ("#147B3D", "#27CB50", "Grass"),
        "electric": Pokemon_type_style ("#E2E32B", "#333333", "Electric"),
        "ice": Pokemon_type_style ("#86D2F5", "#D8F0FA", "Ice"),
        "fighting": Pokemon_type_style ("#994025", "#EF6239", "Fighting"),
        "poison": Pokemon_type_style ("#5E2D89", "#9B69DA", "Poison"),
        "ground": Pokemon_type_style ("#A8702D", "#6E491F", "Ground"),
        "flying": Pokemon_type_style ("#4A677D", "#94B2C7", "Flying"),
        "psychic": Pokemon_type_style ("#A52A6C", "#F71D92", "Psychic"),
        "bug": Pokemon_type_style ("#1C4B27", "#3C9950", "Bug"),
        "rock": Pokemon_type_style ("#48190B", "#8B3E22", "Rock"),
        "ghost": Pokemon_type_style ("#33336B", "#906791", "Ghost"),
        "dragon": Pokemon_type_style ("#448A95", "#62CAD9", "Dragon"),
        "dark": Pokemon_type_style ("#040707", "#595978", "Dark"),
        "steel": Pokemon_type_style ("#60756E", "#43BD94", "Steel"),
        "fairy": Pokemon_type_style ("#961A45", "#E91368", "Fairy")
    }
    return types.get(type_name, Pokemon_type_style("#ccc", "#fff", "Unknown Type"))
