from langchain.tools import tool
from pytrends.request import TrendReq

class TrendsTools():

  @tool("GoogleTrendsTool")
  def trending_searches_on_google(niche):
    """A tool to fetch trending Google searches in a given niche."""
    try:
        pytrends = TrendReq(hl='en-US', tz=360) 
        # Build payload for the keyword
        pytrends.build_payload([niche], cat=0, timeframe='today 1-m', geo='US', gprop='')
        # Get related queries
        related_queries = pytrends.related_queries()
        #print("Google trend search: {}".format(related_queries[niche]['top']))
        return related_queries[niche]['top']
    except Exception as e:
        return f"An error occurred: {str(e)}"
