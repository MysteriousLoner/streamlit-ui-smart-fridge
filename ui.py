import streamlit as st

left_column, right_column = st.columns(2)

chosen = ""

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

    # Display recommendation text
    st.write(
        "Based on the images provided, these are the food I have left in the fridge. "
        "Recommend me what I can cook with these ingredients, prioritizing ingredients that can be consumed completely. "
        f"I have {adults} adults and {children} children aged {ages_str} . The food prepared has to adhere to the {chosen} diet."
    )
