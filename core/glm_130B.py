
import json
import requests

from config import glm_130B_config

def base_strategy_search(prompt, max_length, temperature, top_k, top_p, stop_words, presence_penalty, frequency_penalty):
    request_url = "https://pretrain.aminer.cn/api/v2/completions"
    headers = {'Content-Type': 'application/json'}
    data = {
        "apikey": glm_130B_config.api_key,
        "apisecret": glm_130B_config.api_secret,
        "model": "glm",
        "language": "zh-CN",
        "prompt": prompt,
        "max_tokens": max_length,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "echo": 0,
        "stop": stop_words,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty
    }
    response = requests.post(request_url, headers=headers, data=json.dumps(data))

    if response:
        json_response = response.json()
        if json_response["status"] == 0:
            if "output" in json_response["result"] and json_response["result"]["output"]["errcode"] == 0:
                return json_response["result"]["output"]["raw"].split("<|startofpiece|>")[-1:]

    return None
