import requests

def local_chat_bot(prompt, history=None):
    api = "abc123"
    url = "http://127.0.0.1:1234/v1/chat/completions"

    if history is None:
        history = []
    sys_msg=[{
            "role": "system",
            "content": "You have read all Wikipedia info and give answers in one line for any question."
        }]
    messages =sys_msg+ history + [{"role": "user", "content": prompt.strip()}]
    
    headers = {
        "Authorization": f"Bearer {api}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "Phi 4 Mini Reasoning",
        "messages": messages
    }

    response = requests.post(url, json=data, headers=headers)

    try:
        res = response.json()
    except Exception:
        return "❌ Could not parse local LLM response"

    if "choices" not in res:
        return f"❌ Local LLM Error:\n{res}"

    return res["choices"][0]["message"]["content"]
