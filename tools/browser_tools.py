import os
import requests
from bs4 import BeautifulSoup

from langchain.tools import tool
from groq import Groq

from dotenv import load_dotenv
load_dotenv()

class BrowserTools():

  model = os.getenv('MODEL')
  if not model:
      raise ValueError("MODEL environment variable is not set.")
  groqClient = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
  
  @tool("Scrape website content")
  def scrape_and_summarize_website(url):
    """Scrapes and summarizes the content on the given website. Just pass a string with
    only the full url, without slash `/` at the end, eg: https://google.com or https://clearbit.com/about-us.
    
    Parameters:
        url (str): website url to be scraped. Cannot be empty or None.    
    """

    website = url
    html_content = BrowserTools.fetch_website_html(website)
    if html_content:
        text = BrowserTools.extract_text(html_content)
        chunks = [text[i:i + 8000] for i in range(0, len(text), 8000)]

        summaries = []
        for chunk in chunks:
            chat_completion = BrowserTools.groqClient.chat.completions.create(
                messages = [
                    {
                        "role": "user",
                        "content": f"Analyze and make a LONG summary the content below, make sure to include the ALL relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}",
                    }
                ],
                model = BrowserTools.model,
            )
            
            summaries.append(chat_completion.choices[0].message.content)
            content = "\n\n".join(summaries)
        
        return "Scrapped content: " + content
        return f'\nScrapped Content: {content}\n'
    else:
        return "Failed to fetch content."
  
  def fetch_website_html(url):
      try:
          response = requests.get(url)
          response.raise_for_status()
          return response.text
      except requests.RequestException as e:
          print(f"Error fetching the website: {e}")
          return None

  def extract_text(html_content):
      soup = BeautifulSoup(html_content, 'html.parser')
      text = ' '.join(soup.stripped_strings)
      return text