import requests
import hideee as hide

URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {hide.groq_api}",
    "Content-Type": "application/json"
}

def get_groq_response(user_message):
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }
    
    response = requests.post(URL, headers=HEADERS, json=data)
    response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"]


if __name__ == "__main__":
    print(get_groq_response("Hello, how are you?"))
