import streamlit as st
from gradio_client import Client

# Set up the Gradio client
client = Client("https://cd25840ad2cbe60906.gradio.live/")

# Streamlit App
st.title("Product Description Generator")

# Input fields
product_name = st.text_input("Product Name", "")
features = st.text_area("Features", "")
audience = st.text_area("Target Audience", "")

# Button to generate description
if st.button("Generate Description"):
    if product_name and features and audience:
        with st.spinner("Generating description..."):
            try:
                # Call the Gradio API
                result = client.predict(
                    product_name=product_name,
                    features=features,
                    audience=audience,
                    api_name="/predict"
                )

                # Show the result in Streamlit as a code block
                st.success("Description Generated!")
                st.code(result, language='text')

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please fill in all fields.")
