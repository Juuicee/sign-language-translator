# app.py
import streamlit as st
from PIL import Image
import numpy as np
from tensorflow import keras

# Load the model
model = keras.models.load_model('model.h5')

# Set page config
st.set_page_config(page_title='ASL Interpreter', page_icon=':hand:')

# Title
st.title("Sign Language Recognition")

st.markdown("""
    <div>
        Welcome to the American Sign Language Recognition app! Please upload an image of a hand signing a letter from the ASL alphabet.
        The model will then predict the corresponding letter. Follow the steps listed below:
    </div>
""", unsafe_allow_html=True)

# Instructions
st.subheader('Instructions')
st.text('1. Select "Browse Files" to upload an image of a hand signing a letter \n'
        '2. Wait for the AI to process and display the prediction.\n'
        "3. View the uploaded image and the model's prediction below.")

# Add file uploader to allow users to upload images
uploaded_file = st.file_uploader("Upload an image...", type=["png", "jpg", "jpeg"])

# Get the expected input shape of the model
input_shape = model.input_shape[1:]

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('L')  # Convert image to grayscale
    img = image.resize(input_shape[:2])  # Resize the image to match the input shape
    img_array = np.array(img)
    img_array = img_array / 255.0  # Scale image pixels to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = np.expand_dims(img_array, axis=-1)  # Add single channel dimension

    # Make a prediction
    prediction = model.predict(img_array)

    # Display the prediction
    predicted_class = np.argmax(prediction)
    st.markdown(f'<h2>Prediction: {alphabet[predicted_class]}</h2>', unsafe_allow_html=True)


    # Display the uploaded image
    st.image(image, caption='Uploaded Image.', use_column_width=True)
