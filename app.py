import streamlit as st
import pandas as pd

# Page Setup (The title that appears in the browser tab)
st.set_page_config(page_title="Wicked Weezy Search", layout="wide")

# Main Title (The big header on the page)
st.title("🎤 Wicked Weezy Song List Search Tool")
st.markdown("Type an artist or song name below to search the library.")

# Load Data
@st.cache_data
def load_data():
    # Ensure this matches the filename you uploaded to GitHub!
    return pd.read_csv("SongList.csv", keep_default_na=False)

try:
    df = load_data()
    
    # Search Bar
    search_term = st.text_input("Search:", placeholder="e.g. Bon Jovi or Living on a Prayer")

    # Filter Logic
    if search_term:
        mask = (df['Artist'].str.contains(search_term, case=False, regex=False)) | \
               (df['Song'].str.contains(search_term, case=False, regex=False))
        results = df[mask]
        
        st.success(f"Found {len(results)} matches:")
        
        # Show Results (Hiding ID/Path columns for a cleaner look)
        st.dataframe(results[['Artist', 'Song']], use_container_width=True, hide_index=True)
    else:
        st.info("Enter text to start searching!")

except FileNotFoundError:
    st.error("Song list not found! Please ask the DJ to upload 'SongList.csv'.")
