import requests
import json
from dotenv import load_dotenv,find_dotenv
import os

success_html_path = 'Templates/success.html'

def genai_query(name):
   # Query to pass to AI:
  query = {
    'Performance_Testing_Report':'Analyze the performance test result data generate by Jmeter and suggest some initial analysis & performance engineering.',
    'Code_Analysis_Report':'Analyze the java code and find code level issue related to performance, security, dependency analsysis',
    'Sustainability_Monitor_Repor':'Analyze the system power consumotion and suggest ways to move towards Sustainable applciaiton devoplement ',
    'Accessibility_Testing_Report':'Analyze the Accessibility Testing Report and provide ways for improving Accessibility of the applicaiton'
  }
  return query.get(name,"Analyze the give data and provide insights")

# Function to process files and folders
def process_file_or_folder(file_name):
    content_chunks = []

    # Check if the given name is a file
    if os.path.isfile(file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                words = content.split()

                # Split the content into chunks of 200 words
                for i in range(0, len(words), 200):
                    chunk = ' '.join(words[i:i+200])
                    content_chunks.append({
                        "content": chunk,
                        "role": "user"
                    })
        except UnicodeDecodeError:
            print(f"Skipping file {file_name} due to encoding error.")
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")

    # Check if the given name is a folder (no file extension)
    elif os.path.isdir(file_name):
        for root, dirs, files in os.walk(file_name):
            for file in files:
                # Skip files with certain extensions
                if file.endswith(('.txt', '.png', '.jpeg', '.jpg')):
                    continue

                # Full path of the file
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as file_obj:
                        content = file_obj.read()
                        words = content.split()

                        # Split the content into chunks of 200 words
                        for i in range(0, len(words), 200):
                            chunk = ' '.join(words[i:i+200])
                            content_chunks.append({
                                "content": chunk,
                                "role": "user"
                            })
                except UnicodeDecodeError:
                    print(f"Skipping file {file_path} due to encoding error.")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    else:
        print(f"{file_name} is neither a valid file nor a directory.")

    return content_chunks

def get_env_value(key, env_file='.env', token_file='/Users/bharathkumarm/Docker/AI/token.txt'):
    """
    Fetches the value of a key from a .env file, token.txt, or the current shell session.

    :param key: The environment variable key to fetch.
    :param env_file: Path to the .env file (default is '.env').
    :param token_file: Path to the token file (default is 'token.txt').
    :return: The value of the environment variable or token, or None if the key is not found.
    """
    # First, check if the key is "ACCESS_TOKEN" and try to get it from token.txt
    if os.path.exists(token_file):
        with open(token_file, 'r') as file:
            first_line = file.readline().strip()
            # Split by '=' and check if the key matches
            if first_line.startswith(key + "="):
                return first_line.split('=')[1].strip()

    # Attempt to load the .env file if it exists
    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
    else:
        # Use the default search mechanism for a .env file if not explicitly provided
        load_dotenv(find_dotenv())

    # Fetch the value of the key, either from the .env file or the shell environment
    return os.getenv(key)

def lab45_ai_request(chunks):
  url = "https://api.lab45.ai/v1.1/skills/completion/query"

  payload_data = {
        "messages": [
            {
                "role": "system",
                "content": "you are Data analysis expert "
            },
            *chunks,  # Add the chunks read from the files
            {
                "content": "Provide analysis report based on the given content",
                "role": "user"
            }
        ],
        "search_provider": "Bing",
        "stream_response": False,
        "skill_parameters": {
            "max_output_tokens": 256
        }
    }

  payload = json.dumps(payload_data)

  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {get_env_value('ACCESS_TOKEN')}'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  # Parse the JSON response
  if response.status_code == 200:
    try:
        response_data = response.json()  # Parse the response JSON
        return(response_data['data']['content'])  # Access the nested 'data' -> 'content'
    except KeyError:
        print("The key 'data' or 'content' does not exist in the response.")
    except json.JSONDecodeError:
        print("Failed to decode the response as JSON.")
  else:
    return("System not available at this moment.")


def main():
  # List of file names to process
  file_names = {
    'Performance_Testing_Report':'/Users/bharathkumarm/Docker/JmeterScript/jmeter-report/html-report/statistics.json',
    'Code_Analysis_Report':'/Users/bharathkumarm/Docker/wordsmith/api',
    'Sustainability_Monitor_Repor':'sustainability_metrics.log',
    'Accessibility_Testing_Report':'accessibility_report.csv'
  }

  # Iterate over each file in the list
  for testing_name,file_name in file_names.items():

    # Get the content chunks
    chunks = process_file_or_folder(file_name)
    chunks.append({
              "content": f"from file {file_name} and {genai_query(testing_name)},",
              "role": "user"
            })
    data = lab45_ai_request(chunks)

    # Read success.html, replace placeholder, and write output to the same file
    with open(success_html_path, "r") as file:
      success_html = file.read()

    # Replace placeholder with generated HTML table
    updated_html = success_html.replace(testing_name, data)

    # Save the modified HTML content back to success.html
    with open(success_html_path, "w") as file:
      file.write(updated_html)

    print(f"GenAI Results for {testing_name} inserted into 'success.html'")

if __name__ == '__main__':
    main()