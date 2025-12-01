import httpx
import streamlit as st

# ----- API Key from Streamlit Secrets -----
st.set_page_config(
    page_title="G-ChatBot",
    layout="wide"
)

SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
if not SERPER_API_KEY:
 st.error("SERPER_API_KEY not found in Streamlit Secrets!")
 st.stop()

# ----- Google Search Function -----

async def google_search(query: str):
 url = "[https://google.serper.dev/search](https://google.serper.dev/search)"
 payload = {"q": query}
 headers = {
 "X-API-KEY": str(SERPER_API_KEY),
 "Content-Type": "application/json"
 }


 async with httpx.AsyncClient() as client:
    response = await client.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# ----- Streamlit App -----

st.title("Google Search ChatBot (Serper API)")

query = st.text_input("Enter your question:")

if st.button("Ask"):
 if not query.strip():
  st.warning("Please enter a question!")
 else:
  import asyncio
 try:
    data = asyncio.run(google_search(query))
    answer = data.get("organic", [{}])[0].get("snippet", "No result found.")
    st.markdown(f"**Answer:** {answer}")
    st.info("Source: Google Search (Serper API)")
 except httpx.HTTPStatusError as e:
    st.error(f"API Error {e.response.status_code}: {e}")
 except Exception as e:
    st.error(f"Error: {e}")

