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
        
        # This block DOES need the 'f' because we inject {encoded} and {width}
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
            # --- NO RESULTS FOUND SECTION ---
            st.warning("No results found. Try checking your spelling or switching back to 'All'.")
            
            # FIX: Removed the 'f' from the start of this string so Python
            # doesn't get confused by the CSS variables.
            st.markdown("""
            <div style="
                text-align: center; 
                margin-top: 20px; 
                padding: 20px; 
                background-color: var(--secondary-background-color); 
                border-radius: 10px;
                border: 1px solid var(--text-color-20);">
                
                <p style="font-size: 16px; color: var(--text-color);"><b>Can't find what you're looking for?</b></p>
                
                <a href="https://docs.google.com/forms/d/e/1FAIpQLSf9aQ6xXhr77_ORtb0Q41hLJn7RvycI-ZS5hQdt33q58zvVMA/viewform" target="_blank">
                    <button style="
                        background-color: #FF4B4B; 
                        color: white; 
                        padding: 10px 24px; 
                        border: none; 
                        border-radius: 4px; 
                        cursor: pointer; 
                        font-size: 16px;
                        font-weight: bold;">
                        📝 Request a Song Here
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.info("Enter text above to see results!")

except FileNotFoundError:
    st.error("Song list not found! Please ask the DJ to upload 'SongList.csv' to GitHub.")
