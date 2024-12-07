import streamlit as st
from gradio_client import Client, handle_file
from PIL import Image

# Initialize Gradio clients
image_client = Client("doevent/Face-Real-ESRGAN")
description_client = Client("https://cd25840ad2cbe60906.gradio.live/")

# Streamlit App
st.set_page_config(page_title="Multi-Function App", layout="centered")

# Custom CSS for background color
st.markdown(
    """
    <style>
        /* Set background color */
        body {
            background-color:  #601EF9; /* Sea Blue */
        }
        /* Set text color for better visibility */
        .stApp {
            background-color:  #601EF9; /* Sea Blue */
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Add clickable link at the top
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <a href="techhtml.html" target="_blank" style="font-size: 18px; color: white; text-decoration: none;">
            Click here to Go back to Main Site
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# App Title
st.title("Multi-Function App")

# User selects the feature
feature = st.radio("Choose a feature", ["Image Enhancement", "Product Description Generator"], index=0)

# IMAGE ENHANCEMENT SECTION
if feature == "Image Enhancement":
    st.header("Image Enhancement (ESRGAN)")

    # File uploader for ESRGAN
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        # Select resolution model
        resolution_model = st.radio("Select Resolution Model", ["2x", "4x", "8x"], index=0)

        # Button to enhance the image
        if st.button("Enhance Image"):
            with st.spinner("Enhancing image..."):
                try:
                    # Save uploaded file to a temporary location
                    temp_file_path = f"temp_{uploaded_file.name}"
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.read())

                    # Use Gradio's `handle_file` to prepare the file input
                    result = image_client.predict(
                        image=handle_file(temp_file_path),
                        size=resolution_model,
                        api_name="/predict"
                    )

                    # Handle the response (file path)
                    if isinstance(result, str):
                        # Load the enhanced image from the file path
                        enhanced_image = Image.open(result)

                        # Display the enhanced image
                        st.success("Image Enhanced!")
                        st.image(enhanced_image, caption="Enhanced Image", use_container_width=True)

                        # Provide download button
                        with open(result, "rb") as file:
                            st.download_button(
                                label="Download Enhanced Image",
                                data=file,
                                file_name=f"enhanced_{uploaded_file.name}",
                                mime="image/png",
                            )
                    else:
                        st.error("Unexpected response format from the API.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# PRODUCT DESCRIPTION GENERATOR SECTION
elif feature == "Product Description Generator":
    st.header("Product Description Generator")

    # Input fields with placeholders
    product_name = st.text_input("Product Name", placeholder="Handwoven silk saree")
    features = st.text_area("Features", placeholder="Intricate patterns, vibrant colors, eco-friendly material")
    audience = st.text_area("Target Audience", placeholder="Fashion-conscious individuals, environmentally aware customers")

    # Button to generate description
    if st.button("Generate Description"):
        if product_name and features and audience:
            with st.spinner("Generating description..."):
                try:
                    # Call the Gradio API
                    result = description_client.predict(
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
