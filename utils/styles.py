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
    return Pokemon_type_style(types[type_name][0], types[type_name][1], type_name.capitalize()) if type_name in types else ""

types = {
        "normal": ("#c996a5", "#6f525a"),
        "fire": ("#ae1d26", "#FD4B5A"),
        "water": ("#1552E1", "#85A8FB"),
        "grass": ("#147B3D", "#27CB50"),
        "electric": ("#E2E32B", "#333333"),
        "ice": ("#86D2F5", "#D8F0FA"),
        "fighting": ("#994025", "#EF6239"),
        "poison": ("#5E2D89", "#9B69DA"),
        "ground": ("#A8702D", "#6E491F"),
        "flying": ("#4A677D", "#94B2C7"),
        "psychic": ("#A52A6C", "#F71D92"),
        "bug": ("#1C4B27", "#3C9950"),
        "rock": ("#48190B", "#8B3E22"),
        "ghost": ("#33336B", "#906791"),
        "dragon": ("#448A95", "#62CAD9"),
        "dark": ("#040707", "#595978"),
        "steel": ("#60756E", "#43BD94"),
        "fairy": ("#961A45", "#E91368")
    }