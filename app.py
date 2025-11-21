import streamlit as st
import pandas as pd
import os
import base64

# Page Setup
st.set_page_config(page_title="Wicked Weezy Search", layout="wide")

# --- HELPER: CENTER IMAGE ON ALL DEVICES ---
def render_centered_image(filename, width=300):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
        
        st.markdown(
f"""
<div style="display: flex; justify-content: center; margin-bottom: 20px;">
    <img src="data:image/png;base64,{encoded}" width="{width}">
</div>
""",
            unsafe_allow_html=True
        )
        return True
    return False

# --- LOGO SECTION ---
if not render_centered_image("logo.png"):
    if not render_centered_image("logo.jpg"):
        render_centered_image("logo.JPG")

# --- CENTERED TITLE ---
st.markdown("<h1 style='text-align: center;'>Karaoke Song List Search Tool</h1>", unsafe_allow_html=True)

# Instructions
st.markdown("""
<div style='text-align: center;'>
<b>How to use:</b> Type in the box below to find your karaoke track.<br>
<i>By default, we search for matches in both Artist and Song names.</i>
</div>
""", unsafe_allow_html=True)

st.write("") # Spacer

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("SongList.csv", keep_default_na=False)

try:
    df = load_data()
    
    # Search Input
    search_term = st.text_input("Type here to search:", placeholder="e.g. Journey or Don't Stop Believin'")

    # Filter Options
    col1, col2 = st.columns([1, 2])
    
    with col1:
        search_mode = st.radio(
            "Optional: Narrow your search:",
            ["All (Default)", "Artist Name Only", "Song Title Only"],
            horizontal=False
        )

    # --- SMART FILTER LOGIC ---
    if search_term:
        # 1. Split the search into individual words (tokens)
        # "Bon Jovi Livin" -> ["Bon", "Jovi", "Livin"]
        search_tokens = search_term.split()
        
        # 2. Start with a mask that includes ALL rows (True)
        mask = pd.Series(True, index=df.index)

        # 3. Loop through each word and narrow down the results
        for token in search_tokens:
            if search_mode == "All (Default)":
                # Keep row if token is in Artist OR Song
                mask = mask & (
                    df['Artist'].str.contains(token, case=False, regex=False) | 
                    df['Song'].str.contains(token, case=False, regex=False)
                )
            elif search_mode == "Artist Name Only":
                # Keep row only if token is in Artist
                mask = mask & df['Artist'].str.contains(token, case=False, regex=False)
            else:
                # Keep row only if token is in Song
                mask = mask & df['Song'].str.contains(token, case=False, regex=False)
        
        # Apply the final mask
        results = df[mask]
        
        st.divider()
        
        if len(results) > 0:
            st.success(f"Found {len(results)} matches:")
            st.dataframe(results[['Artist', 'Song']], use_container_width=True, hide_index=True)
        else:
            # --- NO RESULTS FOUND SECTION ---
            st.warning("No results found. Try checking your spelling or switching back to 'All'.")
            
            st.markdown(
"""
<div style="text-align: center; margin-top: 20px; padding: 20px; background-color: var(--secondary-background-color); border-radius: 10px; border: 1px solid var(--text-color-20);">
    <p style="font-size: 16px; color: var(--text-color);"><b>Can't find what you're looking for?</b></p>
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSf9aQ6xXhr77_ORtb0Q41hLJn7RvycI-ZS5hQdt33q58zvVMA/viewform" target="_blank">
        <button style="background-color: #FF4B4B; color: white; padding: 10px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold;">
            📝 Request a Song Here
        </button>
    </a>
</div>
""", 
                unsafe_allow_html=True
            )
            
    else:
        st.info("Search our Song Library to find out what to sing!")

except FileNotFoundError:
    st.error("Song list not found! Please ask the DJ to upload 'SongList.csv' to GitHub.")
