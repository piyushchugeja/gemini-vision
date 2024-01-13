import google.generativeai as genai
import streamlit as st
import PIL.Image

# configure GenAI and initialise model
genai.configure(
    api_key=st.secrets["GOOGLE_API_KEY"],
)
model = genai.GenerativeModel("gemini-pro-vision")

st.set_page_config(
    page_title = "Vision",
    page_icon = "👁️",
    layout = "wide",
    initial_sidebar_state = "collapsed",
)

st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(2) {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Gemini Vision 👁️")
st.write("Provide an image and a prompt which instructs the AI on what to do with the image. The AI will then generate an output based on the prompt.")

if 'image' not in st.session_state:
    st.session_state.image = None

col1, col2 = st.columns(2)

with col1:
    img_raw = st.file_uploader("Upload your image here", type=["png", "jpg", "jpeg"])
    prompt = st.text_area("Enter your prompt here", placeholder="e.g. Identify the main object in the image and write a blog on it")
    button = st.button("Launch")
    
with col2:
    if img_raw:
        st.image(img_raw, use_column_width=True)
    else:
        st.subheader("Your image will be displayed here")
    


if button:
    with st.spinner("Processing..."):
        try:
            if img_raw and prompt:
                st.session_state.image = PIL.Image.open(img_raw)
                response = model.generate_content(
                    contents = [prompt, st.session_state.image]
                )
                st.success(response.text)
            elif not img_raw:
                st.error("Please upload an image.")
                st.session_state.image = None
            elif not prompt:
                st.error("Please enter a prompt.")
        except Exception as e:
            print(e)
            st.error("Something went wrong. Please try again.")