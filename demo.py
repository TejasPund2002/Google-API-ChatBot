# import httpx
# import streamlit as st

# # ----- API Key from Streamlit Secrets -----
# st.set_page_config(
#     page_title="G-ChatBot",
#     layout="wide"
# )

# SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
# if not SERPER_API_KEY:
#  st.error("SERPER_API_KEY not found in Streamlit Secrets!")
#  st.stop()

# # ----- Google Search Function -----

# async def google_search(query: str):
#  url = "https://google.serper.dev/search"
#  payload = {"q": query}
#  headers = {
#  "X-API-KEY": str(SERPER_API_KEY),
#  "Content-Type": "application/json"
#  }


#  async with httpx.AsyncClient() as client:
#     response = await client.post(url, json=payload, headers=headers)
#     response.raise_for_status()
#     return response.json()

# # ----- Streamlit App -----

# st.title("Google Search ChatBot (Serper API)")

# query = st.text_input("Enter your question:")

# if st.button("Ask"):
#  if not query.strip():
#   st.warning("Please enter a question!")
#  else:
#   import asyncio
#  try:
#     data = asyncio.run(google_search(query))
#     answer = data.get("organic", [{}])[0].get("snippet", "No result found.")
#     st.markdown(f"**Answer:** {answer}")
#     st.info("Source: Google Search (Serper API)")
#  except httpx.HTTPStatusError as e:
#     st.error(f"API Error {e.response.status_code}: {e}")
#  except Exception as e:
#     st.error(f"Error: {e}")


import httpx
import streamlit as st
import asyncio

# ----- Page Config -----
st.set_page_config(
    page_title="G-ChatBot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----- Background & CSS -----
st.markdown(
    """
    <style>
    /* Background Image */
    .stApp {
        background-image: url('https://pin.it/3dTm6TqBb');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    /* Card for answer */
    .answer-card {
        background: rgba(0, 0, 50, 0.75);
        padding: 20px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        margin-top: 20px;
    }

    /* Styled input */
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
        border: 2px solid #1f77b4;
        box-shadow: 0 0 10px rgba(31, 119, 180, 0.5);
        color: #000;
    }

    /* Styled button */
    div.stButton>button {
        background-color: #1f77b4;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }

    div.stButton>button:hover {
        background-color: #105a8b;
        transform: scale(1.05);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0,0,50,0.8);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
def set_bg_from_local(image_file):
    import base64
    with open(image_file, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{b64}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Usage
set_bg_from_local("download.jpeg")

# ----- API Key from Streamlit Secrets -----
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
if not SERPER_API_KEY:
    st.error("SERPER_API_KEY not found in Streamlit Secrets!")
    st.stop()

# ----- Google Search Function -----
async def google_search(query: str):
    url = "https://google.serper.dev/search"
    payload = {"q": query}
    headers = {
        "X-API-KEY": str(SERPER_API_KEY),
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

# ----- Streamlit UI -----
st.markdown("<h1 style='color:white;text-align:center'>🤖 G-ChatBot</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:white;text-align:center'>Ask any question and get AI-powered search results instantly!</p>", unsafe_allow_html=True)



st.markdown("""
<style>
/* Targets the input element within the stTextInput container */
.stTextInput input[aria-label="Black and White Input"] {
    background-color: #000000; /* Black background */
    color: #FFFFFF;            /* White text color */
    border: 1px solid #FFFFFF; /* Optional: adds a white border */
    font-size: 16px;           /* Optional: change font size */
}

/* Optional: change the label color to white for better visibility on a dark app background */
.stMarkdown p {
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

query = st.text_input("Type Your Question here")

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question!")
    else:
        with st.spinner("Fetching answer from Google Search..."):
            try:
                data = asyncio.run(google_search(query))
                answer = data.get("organic", [{}])[0].get("snippet", "No result found.")
                st.markdown(f"<div class='answer-card'><h3>Answer:</h3><p>{answer}</p></div>", unsafe_allow_html=True)
            except httpx.HTTPStatusError as e:
                st.error(f"API Error {e.response.status_code}: {e}")
            except Exception as e:
                st.error(f"Error: {e}")














