import streamlit as st

import utils.api as api
import utils.charts as charts
import utils.ui_blocks as ui_blocks

#App title
st.title("PokeDex")

#App subtitle
st.subheader("By Alphalejo")

#Select Function
function = st.pills(
    label="Select Function",
    options=["Information", "Compare", "VS", "Team Generator"],
    selection_mode="single",
    default="Information",
)

if function == "Information":

    # Select asset type
    # take the selected option selected and convert it to lowercase
    asset = str(st.pills(
        label="Select Asset Type",
        options=["Pokemon", "Berry", "Item", "Location"],
        selection_mode="single",
        default="Pokemon",)
    ).lower()

    #input for asset name
    asset_name = str(st.selectbox(
        "Enter the name of a Pokemon:",
        options=api.all_pokemon_names())
    )
    # Display the Pokemon data
    if asset_name:
        #print(asset, asset_name) # Debugging line to check the asset and name
        
        if asset == "pokemon":
            ui_blocks.pokemon_data(asset, asset_name)
                
        else:
            st.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages-wixmp-ed30a86b8c4ca887773594c2.wixmp.com%2Ff%2F5d593771-5eab-464a-91a2-1e4af6b88b2f%2Fddrl3x8-f0050a0d-450f-4394-b71b-8bccef18504d.png%2Fv1%2Ffill%2Fw_640%2Ch_256%2Cstrp%2Fpokemon_berries_1_10_128px_artworks_by_anarlaurendil_ddrl3x8-fullview.png%3Ftoken%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MjU2IiwicGF0aCI6IlwvZlwvNWQ1OTM3NzEtNWVhYi00NjRhLTkxYTItMWU0YWY2Yjg4YjJmXC9kZHJsM3g4LWYwMDUwYTBkLTQ1MGYtNDM5NC1iNzFiLThiY2NlZjE4NTA0ZC5wbmciLCJ3aWR0aCI6Ijw9NjQwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.8luKHvaPYn40DvpnqJ186noQ7b5Y9JvW7zRQ1QO3-P0&f=1&nofb=1&ipt=8ea3b6307cd1d50b64b6382a52f0aef30b44d97840a1b164f650af7a33102755")

elif function == "Compare":
    
    ui_blocks.compare_dashboard()

elif function == "VS":
    
    ui_blocks.vs_dashboard()

elif function == "Team Generator":
    st.write("Team Generator functionality is not implemented yet.")

else:
    st.write("Please select a valid function.")