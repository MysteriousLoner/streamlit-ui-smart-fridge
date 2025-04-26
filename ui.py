import streamlit as st
from google import genai
from google.genai import types
import os

GOOGLE_API_KEY=""

left_column, right_column = st.columns(2)
prompt =""
chosen = ""
uploaded_image = None
client = genai.Client(api_key=GOOGLE_API_KEY)
save_path = ""

def reset_custom_text():
    st.session_state.custom_text = ""

# Using Streamlit functions inside a "with" block
with right_column:
    chosen = st.radio(
        'Dietary options',
        ("vegan", "kosher", "halal", "high protein"),
        on_change=reset_custom_text
    )
    custom = st.text_input("Other diet form, please specify", key="custom_text")
    if custom != "":
        chosen = custom

    # Add an image upload widget
    uploaded_image = st.file_uploader("Upload an image of your fridge contents", type=["jpg", "png", "jpeg"])

   # Display the uploaded image
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded image", use_container_width=True)

    # Define the path to save the uploaded file in the project root
    save_path = os.path.join(os.getcwd(), "temp_image.jpg")

    if uploaded_image is not None:
        # Save the uploaded file to the project root
        with open(save_path, "wb") as f:
            f.write(uploaded_image.getbuffer())

        st.write(f"File saved successfully to {save_path}!")
    

with left_column:
    adults = st.text_input("Number of Adults")
    children = st.text_input("Number of Children", value="0")

    # Convert input to integer
    try:
        num_children = int(children) if children.isdigit() else 0
    except ValueError:
        num_children = 0

    # Create sliders for children's ages dynamically
    children_ages = []
    if num_children > 0:
        st.write("Select the age for each child:")
        for i in range(num_children):
            age = st.slider(f"Age of Child {i+1}", min_value=0, max_value=18, value=5)
            children_ages.append(age)

    ages_str = ", ".join(map(str, children_ages)) if children_ages else "N/A"

    # recommendation text
    st.write(
        "Based on the images provided, these are the food I have left in the fridge. "
        "Recommend me what I can cook with these ingredients, prioritizing ingredients that can be consumed completely. "
        f"I have {adults} adults and {children} children aged {ages_str} . The food prepared has to adhere to the {chosen} diet."
    )

    prompt = (
        "Based on the images provided, these are the food I have left in the fridge. "
        "Recommend me what I can cook with these ingredients, prioritizing ingredients that can be consumed completely. "
        f"I have {adults} adults and {children} children aged {ages_str} . The food prepared has to adhere to the {chosen} diet."
    )


# Add a button to trigger content generation
if st.button("Generate Content"):
    if uploaded_image is not None:
        with open(save_path, 'rb') as f:
            image_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
            ), prompt],
        )
        st.write("Generated Response:")
        st.write(response.text)
    else:
        st.warning("Please upload an image before generating content.")