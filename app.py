# Import necessary libraries
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Setup Streamlit app
st.set_page_config(page_title="PySweep Pro", layout="wide")
st.title("🐍 PySweep Pro")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        st.write(f"**File Extension:** {file_ext}")

        # Read the file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Show preview
        st.write("📌 **Preview of the DataFrame:**")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"✅ Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            # Remove duplicates
            with col1:
                if st.button(f"🗑️ Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")

            # Fill missing values
            with col2:
                if st.button(f"📥 Fill Missing Values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if numeric_cols.empty:
                        st.warning("⚠️ No numeric columns found!")
                    else:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("✅ Missing values filled!")

        # File Conversion
        st.subheader("📥 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(label=f"⬇️ Download {file_name}", data=buffer, file_name=file_name, mime=mime_type)

