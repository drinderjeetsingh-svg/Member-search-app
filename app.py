import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NZOA Member Portal", page_icon="📋")

st.title("📋 NZOA Membership Search")
st.write("Find your LM number by searching with your Name, Email, or Mobile.")

# --- DATA LOADING ---
file_path = "members.csv"

if not os.path.exists(file_path):
    st.error(f"❌ Error: The file '{file_path}' was not found in the GitHub repository.")
    st.info("Please upload your Excel/CSV file to GitHub and name it 'members.csv'.")
else:
    @st.cache_data
    def load_data():
        # Load the file
        data = pd.read_csv(file_path)
        # Clean up column names (removes accidental spaces)
        data.columns = data.columns.str.strip()
        return data

    try:
        df = load_data()
        
        # --- SEARCH INTERFACE ---
        search_input = st.text_input("Enter Name, Email, or Mobile Number", "").strip()

        if search_input:
            # Flexible search across columns
            mask = (
                df['Name'].astype(str).str.contains(search_input, case=False, na=False) |
                df['Mobile'].astype(str).str.contains(search_input, na=False) |
                df['E mail'].astype(str).str.contains(search_input, case=False, na=False)
            )
            
            results = df[mask]
            
            if not results.empty:
                st.success(f"Matches Found: {len(results)}")
                # Show specific columns in your requested order
                st.dataframe(results[['LM number', 'Name', 'City', 'Mobile', 'E mail']], hide_index=True)
            else:
                st.warning("No member found with those details. Please try again.")
        else:
            st.info("Tip: You can search by partial name or the last 4 digits of a mobile number.")

    except Exception as e:
        st.error(f"An error occurred while reading the data: {e}")
