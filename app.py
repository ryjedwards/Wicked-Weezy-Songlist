import streamlit as st
import pandas as pd
import os

# Page Setup
st.set_page_config(page_title="Wicked Weezy Search", layout="wide")

# --- CENTERED LOGO SECTION ---
left_co, cent_co, last_co = st.columns([1, 2, 1])

with cent_co:
    # PRIORITIZE PNG since that's what you have!
    if os.path.exists("logo.png"):
        st.image("logo.png", width=300)
    elif os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=300)
    elif os.path.exists("logo.JPG"):
        st.image("logo.JPG", width=300)
    else:
        # Fallback text
        st.header("🎤 Wicked Weezy")

# --- CENTERED TITLE ---
st.markdown("<h1 style='text-align: center;'>Song List Search Tool</h1>", unsafe_allow_html=True)

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

    # Filter Logic
    if search_term:
        if search_mode == "All (Default)":
            mask = (df['Artist'].str.contains(search_term, case=False, regex=False)) | \
                   (df['Song'].str.contains(search_term, case=False, regex=False))
        elif search_mode == "Artist Name Only":
            mask = df['Artist'].str.contains(search_term, case=False, regex=False)
        else:
            mask = df['Song'].str.contains(search_term, case=False, regex=False)
            
        results = df[mask]
        
        st.divider()
        
        if len(results) > 0:
            st.success(f"Found {len(results)} matches:")
            st.dataframe(results[['Artist', 'Song']], use_container_width=True, hide_index=True)
        else:
            st.warning("No results found. Try checking your spelling or switching back to 'All'.")
            
    else:
        st.info("Enter text above to see results!")

except FileNotFoundError:
    st.error("Song list not found! Please ask the DJ to upload 'SongList.csv' to GitHub.")
