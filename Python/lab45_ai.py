import requests
import json
from dotenv import load_dotenv
import os

def get_env_value(key, env_file='.env'):
    """
    Reads a .env file and returns the value for the specified key.

    :param key: Key to fetch from the .env file
    :param env_file: Path to the .env file (default is '.env')
    :return: Value of the specified key or None if the key is not found
    """
    # Load the .env file
    load_dotenv(dotenv_path=env_file)

    # Get the value of the key
    return os.getenv(key)

def lab45_ai_request():
  url = "https://api.lab45.ai/v1.1/skills/completion/query"

  payload = json.dumps({
    "messages": [
      {
        "role": "system",
        "content": "you are expert in searching and finding answer"
      },
      {
        "content": "What is a cat?",
        "role": "user"
      }
    ],
    "search_provider": "Bing",
    "stream_response": False,
    "skill_parameters": {
      "max_output_tokens": 256
    }
  })
  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {get_env_value('lab45_token')}'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  # Parse the JSON response
  try:
      response_data = response.json()  # Parse the response JSON
      print(response_data['data']['content'])  # Access the nested 'data' -> 'content'
  except KeyError:
      print("The key 'data' or 'content' does not exist in the response.")
  except json.JSONDecodeError:
      print("Failed to decode the response as JSON.")

lab45_ai_request()