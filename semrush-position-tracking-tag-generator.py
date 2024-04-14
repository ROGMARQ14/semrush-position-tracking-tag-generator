import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO

# Helper functions as defined earlier
def get_new_existing_tag(content_type):
    if "New" in content_type:
        return "New"
    elif "Update" in content_type:
        return "Existing"
    else:
        return "Unknown"

def get_post_page_tag(content_type):
    if "Post" in content_type:
        return "Post"
    elif "Page" in content_type:
        return "Page"
    else:
        return "Unknown"

def format_date(date):
    if isinstance(date, str):
        date_obj = datetime.strptime(date, "%m/%d/%Y")
        return date_obj.strftime("%b%Y").lower()
    return None

def get_table_download_link(df):
    """Generates a link allowing the processed data to be downloaded"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="processed_tags.csv">Download CSV</a>'
    return href

def process_data(file):
    data = pd.read_csv(file)
    
    # Apply the functions to the data
    data['New or Existing'] = data['Content Type'].apply(get_new_existing_tag)
    data['Post or Page'] = data['Content Type'].apply(get_post_page_tag)
    data['Formatted Date'] = data['Date'].apply(format_date)
    
    # Filter out rows where the date could not be formatted
    data = data.dropna(subset=['Formatted Date'])
    
    # Build the full tag for the cleaned data
    data['Full Tag'] = data.apply(
        lambda x: f"{x['Target Keyword']}, {x['Formatted Date']}, {x['New or Existing']}, {x['Post or Page']}", 
        axis=1
    )
    
    # Return only the Full Tag column
    return data[['Full Tag']]

# Streamlit application layout
st.title('SEMRush Position Tracking Tag Generator')
st.write('Upload a CSV file to generate tags for SEMRush position tracking.')

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
if uploaded_file is not None:
    # Process the uploaded file
    processed_data = process_data(uploaded_file)
    
    # Show processed data in the app
    st.write("Processed Data:")
    st.write(processed_data)
    
    # Create download link for the processed data
    st.markdown(get_table_download_link(processed_data), unsafe_allow_html=True)
