import streamlit as st
import pandas as pd

# Page Setup
st.set_page_config(page_title="Karaoke Search", layout="wide")

# Title and Styling
st.title("🎤 Karaoke Song Search")
st.markdown("Type an artist or song name below to search the library.")

# Load Data (Cached so it doesn't reload on every keystroke)
@st.cache_data
def load_data():
    # We assume the DJ uploads a file named 'SongList.csv'
    # 'keep_default_na=False' prevents empty cells from becoming "NaN"
    return pd.read_csv("SongList.csv", keep_default_na=False)

try:
    df = load_data()
    
    # Search Bar
    search_term = st.text_input("Search:", placeholder="e.g. Bon Jovi or Living on a Prayer")

    # Filter Logic
    if search_term:
        # Search in both Artist and Song columns (case insensitive)
        mask = (df['Artist'].str.contains(search_term, case=False, regex=False)) | \
               (df['Song'].str.contains(search_term, case=False, regex=False))
        results = df[mask]
        
        st.success(f"Found {len(results)} matches:")
        
        # Show Results (Hide the confusing 'ID' and 'Path' columns from patrons)
        # Only show Artist and Song
        st.dataframe(results[['Artist', 'Song']], use_container_width=True, hide_index=True)
    else:
        st.info("Enter text to start searching!")

except FileNotFoundError:
    st.error("Song list not found! Please ask the DJ to upload 'SongList.csv'.")
