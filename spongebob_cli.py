#!/usr/bin/env python3
"""
Example: One-shot call to ai.sooners.us using gemma3:4b model.

Requires:
  pip install requests python-dotenv
"""

import os
import requests
from dotenv import load_dotenv

# Load API key and base URL from ~/.soonerai.env
load_dotenv(os.path.join(os.getcwd(), ".soonerai.env"))

API_KEY = os.getenv("SOONERAI_API_KEY")
BASE_URL = os.getenv("SOONERAI_BASE_URL", "https://ai.sooners.us").rstrip("/")
MODEL = os.getenv("SOONERAI_MODEL", "gemma3:4b")

if not API_KEY:
    raise RuntimeError("Missing SOONERAI_API_KEY in ~/.soonerai.env")

# Prepare API request
url = f"{BASE_URL}/api/chat/completions"
payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "You are SpongeBob SquarePants. Speak cheerfully and use ocean humor."}
    ],
    "temperature": 0.6,
}

while(True):
    userIn = input("User: ")
    payload["messages"].append({"role": "user", "content":userIn})

    # Send POST request
    response = requests.post(
    url,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json=payload,
    timeout=60,
    )

    # Display result
    if response.status_code == 200:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        payload["messages"].append({"role": "assistant", "content":reply})
        print("SpongeBob:", reply)
    else:
        print(f"Error {response.status_code}: {response.text}")