import streamlit as st
import pandas as pd

# Page Setup
st.set_page_config(page_title="Wicked Weezy Search", layout="wide")

# Main Title
st.title("🎤 Wicked Weezy Song List Search Tool")

# Instructions
st.markdown("""
**How to use:** Type in the box below to find your karaoke track.  
*By default, we search for matches in both Artist and Song names.*
""")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("SongList.csv", keep_default_na=False)

try:
    df = load_data()
    
    # Search Input
    search_term = st.text_input("Type here to search:", placeholder="e.g. Journey or Don't Stop Believin'")

    # Filter Options (Radio buttons acting as tabs)
    # We use columns to keep the UI tight
    col1, col2 = st.columns([1, 2])
    
    with col1:
        search_mode = st.radio(
            "Optional: Narrow your search:",
            ["All (Default)", "Artist Name Only", "Song Title Only"],
            horizontal=False # Stacked looks better on mobile phones
        )

    # Filter Logic
    if search_term:
        # 1. Search ALL (Default)
        if search_mode == "All (Default)":
            mask = (df['Artist'].str.contains(search_term, case=False, regex=False)) | \
                   (df['Song'].str.contains(search_term, case=False, regex=False))
        
        # 2. Search ARTIST Only
        elif search_mode == "Artist Name Only":
            mask = df['Artist'].str.contains(search_term, case=False, regex=False)
            
        # 3. Search SONG Only
        else:
            mask = df['Song'].str.contains(search_term, case=False, regex=False)
            
        results = df[mask]
        
        st.divider() # Visual separator
        
        if len(results) > 0:
            st.success(f"Found {len(results)} matches:")
            st.dataframe(results[['Artist', 'Song']], use_container_width=True, hide_index=True)
        else:
            st.warning("No results found. Try checking your spelling or switching back to 'All'.")
            
    else:
        st.info("Enter text above to see results!")

except FileNotFoundError:
    st.error("Song list not found! Please ask the DJ to upload 'SongList.csv' to GitHub.")
