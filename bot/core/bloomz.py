
import json
import requests

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloomz"

def generate(prompt, parameters, api_token):
    headers = {"Authorization": f"Bearer " + api_token}
    data = {
        "inputs": prompt,
        "parameters": parameters,
        "options": {
            "use_cache": True,
            "wait_for_model": True
        }
    }

    response = requests.request("POST", API_URL,  headers=headers, json=data)

    if response.status_code == 200:
        json_response = json.loads(response.content.decode("utf-8"))
        return json_response[0]["generated_text"][len(prompt):]

    return None

def sample(prompt, seed, top_p, api_token):
    parameters = {
        "max_new_tokens": 200,
        "top_p": top_p,
        "do_sample": True,
        "seed": seed,
        "early_stopping": False,
        "length_penalty": 0.0,
        "eos_token_id": None
    }
    return generate(prompt, parameters, api_token)

def greedy(prompt, seed, api_token):
    parameters = {
        "max_new_tokens": 200,
        "do_sample": False,
        "seed": seed,
        "early_stopping": False,
        "length_penalty": 0.0,
        "eos_token_id": None
    }

    return generate(prompt, parameters, api_token)
