
import json
import requests

from requests import Response

API_URL: str = "https://api-inference.huggingface.co/models/bigscience/bloom"

def generate(prompt: str, parameters: dict, api_token: str) -> tuple:
    headers: dict = {"Authorization": f"Bearer " + api_token}
    data: dict = {
        "inputs": prompt,
        "parameters": parameters,
        "options": {
            "wait_for_model": True
        }
    }
    response: Response = requests.request("POST", API_URL,  headers=headers, json=data)

    status_code: int = response.status_code
    response_data: dict = None

    if status_code == 200:
        json_response: dict = json.loads(response.content.decode("utf-8"))
        if "error" not in json_response:
            status_code = 0
            response_data = json_response[0]["generated_text"]
        else:
            response_data = json_response["error"]
    else:
        try:
            json_response: dict = json.loads(response.content.decode("utf-8"))
            response_data = json_response["error"]
        except ValueError:
            response_data = response.text
    return status_code, response_data

def sample(prompt: str, max_new_tokens: int, seed: int, temperature: float, top_p: float, api_token: str) -> str:
    parameters: dict = {
        "max_new_tokens": max_new_tokens,
        "do_sample": True,
        "seed": seed,
        "early_stopping": False,
        "length_penalty": 0.0,
        "eos_token_id": None,
        "temperature": temperature,
        "top_p": top_p
    }
    return generate(prompt, parameters, api_token)

def greedy(prompt: str, max_new_tokens: int, seed: int, api_token: str) -> str:
    parameters: dict = {
        "max_new_tokens": max_new_tokens,
        "do_sample": False,
        "seed": seed,
        "early_stopping": False,
        "length_penalty": 0.0,
        "eos_token_id": None
    }
    return generate(prompt, parameters, api_token)
