import streamlit as st
import pandas as pd

st.set_page_config(page_title="LM Search Portal", page_icon="🏢")

st.title("📋 Membership Search Portal")
st.write("Find your LM number by searching with your Name, Email, or Mobile.")

# Load data based on your specific sequence
@st.cache_data
def load_data():
    # Sequence: LM number, Name, City, Mobile, E-mail
    df = pd.read_csv("members.csv")
    return df

df = load_data()

# Search box
search_input = st.text_input("Search by Name, Email, or Mobile Number", "").strip()

if search_input:
    # Logic to search across Name, Mobile, and Email columns
    mask = (
        df['Name'].astype(str).str.contains(search_input, case=False, na=False) |
        df['Mobile'].astype(str).str.contains(search_input, na=False) |
        df['E-mail'].astype(str).str.contains(search_input, case=False, na=False)
    )
    
    results = df[mask]
    
    if not results.empty:
        st.success(f"Found {len(results)} match(es)")
        # Displaying the results in your preferred column order
        st.dataframe(results[['LM number', 'Name', 'City', 'Mobile', 'E-mail']], hide_index=True)
    else:
        st.error("No member found. Please try searching with a different detail.")
else:
    st.info("Results will appear here once you start typing.")
