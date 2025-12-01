import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

SERPER_API_KEY = "0b3e7c0255d581c328c0753267b2ccb4a2682fde"

if not SERPER_API_KEY:
 raise RuntimeError("SERPER_API_KEY environment variable is not set!")

app = FastAPI(title="Google Search ChatBot")

class ChatRequest(BaseModel):
 question: str

async def google_search(query: str):
    url = "https://google.serper.dev/search"
    print("Request URL:", url) 
    payload = {"q": query}
    headers = {
        "X-API-KEY": str(SERPER_API_KEY),
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()


  
# ----- Chat Endpoint -----

@app.post("/chat")
async def chat(req: ChatRequest):
 try:
  data = await google_search(req.question)
 except httpx.HTTPStatusError as e:
  raise HTTPException(status_code=e.response.status_code, detail=str(e))


# Extract best answer
 answer = data.get("organic", [{}])[0].get("snippet", "No result found.")

 return {
      "question": req.question,
      "answer": answer,
      "source": "Google Search (Serper API)"
      }

# ----- Run Instructions -----

# uvicorn main:app --reload

# POST request JSON body: {"question": "What is Artificial Intelligence?"}
