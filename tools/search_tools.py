import json
import os

import requests
from langchain.tools import tool


class SearchTools():

  serper_api_key = os.getenv('SERPER_API_KEY')

  if not serper_api_key:
    raise ValueError("serper api key is not set.")
  
  @tool("Search internet")
  def search_internet(query, n_results=5):
    """Useful to search the internet about a given topic and return relevant
    results."""

    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': SearchTools.serper_api_key,
        'content-type': 'application/json'
    }

    print("url: "+url)
    print("query: "+query)
    print(headers)
    response = requests.request("POST", url, headers=headers, data=payload)
    
    try:
        response_json = response.json()
        print("Response JSON:", response_json)  # Debug: Print the entire response JSON
        
        if 'organic' in response_json:
            results = response_json['organic']
            stirng = []
            for result in results[:n_results]:
                try:
                    stirng.append('\n'.join([
                        f"Title: {result['title']}", f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
                except KeyError:
                    continue

            content = '\n'.join(stirng)
            return f"\nSearch result: {content}\n"
        else:
            return "No organic search results found."
    except json.JSONDecodeError:
        return "Failed to decode the response JSON."
    except Exception as e:
        return f"An error occurred: {str(e)}"