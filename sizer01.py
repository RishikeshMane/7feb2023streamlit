import streamlit as st
from PIL import Image

# Set a title for your app
st.title('SimuVerse by Unruffled Feathers')

# Initialize session state variables if they don't exist
if 'show_input' not in st.session_state:
    st.session_state.show_input = True  # Controls whether to show input form or results

# Toggle function to switch views
def toggle_view():
    st.session_state.show_input = not st.session_state.show_input

# Create a placeholder to store shirt data
if 'shirt_data' not in st.session_state:
    st.session_state.shirt_data = []

# Define the function to add a shirt to the list
def add_shirt(brand, shoulder, length, chest, image):
    st.session_state.shirt_data.append({"Brand": brand, "Shoulder": shoulder, "Length": length, "Chest": chest, "Image": image})

# Function to display matching shirts based on user's dimensions
def recommend_shirts(shoulder, length, chest):
    matches = [shirt for shirt in st.session_state.shirt_data if shirt["Shoulder"] <= shoulder + 1 and shirt["Shoulder"] >= shoulder - 1 and shirt["Length"] <= length + 1 and shirt["Length"] >= length - 1 and shirt["Chest"] <= chest + 1 and shirt["Chest"] >= chest - 1]
    if matches:
        for match in matches:
            st.write(f"Brand: {match['Brand']}, Shoulder: {match['Shoulder']}, Length: {match['Length']}, Chest: {match['Chest']}")
            st.image(match["Image"], width=200)
    else:
        st.write("No matching shirts found.")

# Sidebar logic for showing input or results
if st.session_state.show_input:
    with st.sidebar:
        st.write("## Input Shirt Data")
        brand = st.text_input("Brand")
        shoulder = st.number_input("Shoulder (in inches)", min_value=0.0, format="%.2f")
        length = st.number_input("Length (in inches)", min_value=0.0, format="%.2f")
        chest = st.number_input("Chest (in inches)", min_value=0.0, format="%.2f")
        image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if st.button("Add Shirt"):
            if image:
                image = Image.open(image)
                add_shirt(brand, shoulder, length, chest, image)
                st.success("Shirt added successfully!")
        st.button("Show Recommendations", on_click=toggle_view)
else:
    st.sidebar.write("## Enter Your Dimensions")
    user_shoulder = st.sidebar.slider("Your Shoulder Width (in inches)", min_value=0.0, max_value=50.0, value=18.0, step=0.5)
    user_length = st.sidebar.slider("Your Shirt Length (in inches)", min_value=0.0, max_value=50.0, value=24.0, step=0.5)
    user_chest = st.sidebar.slider("Your Chest Size (in inches)", min_value=0.0, max_value=50.0, value=36.0, step=0.5)
    if st.sidebar.button("Find Matching Shirts"):
        recommend_shirts(user_shoulder, user_length, user_chest)
    st.sidebar.button("Back to Add Shirt", on_click=toggle_view)
