import os
import json
from dotenv import load_dotenv
load_dotenv()
from textwrap import dedent

import tweepy
import re
from groq import Groq
from crewai import  Crew
from crewai.process import Process
from tasks import ViralContentCreationTasks
from agents import ViralContentCreators

tasks = ViralContentCreationTasks()
agents = ViralContentCreators()

print("## Welcome to the Twitter Content Creation Crew")
print('-------------------------------')
niche = input("What is your niche?\n")

model = os.getenv('MODEL')
if not model:
	raise ValueError("MODEL environment variable is not set.")
groqClient = Groq(
	api_key=os.getenv("GROQ_API_KEY"),
)

def get_tweets_from_llm(content):
    chat_completion = groqClient.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": dedent(f"""\
                                  You are helpful assistant that receives some text from the user. 
                                  The text contains a couple of twitter tweets.
                                  You extract all the tweets from the text and create an array of tweets and return
                                  the array without any additional info, explanation, instructions or metadata.
                        """)
            },
            {
                "role": "user",
                "content": dedent(f"""\
                    Generate an array of tweets based on the content below.
                    Return only the array of tweets in the format: ["tweet_1", "tweet_2", ...], where tweet_1 is the
                                  first tweet, tweet_2 is the second tweet and so on, without any explanation or
                                  metadata. Let's call your response to this query as tweets_array. Then this 
                                  python code should work fine on my end: "tweets_list = json.loads(tweets_array)"
                    Content: {content}
                """),
            }
        ],
        model=model,
    )
    
    # Extract the JSON array from the response
    response_text  = chat_completion.choices[0].message.content
    match = re.search(r'\[(.*?)\]', response_text , re.DOTALL)
    
    if match:
        tweets_array = '[' + match.group(1) + ']'
        try:
            print("tweets_array: ")
            print(tweets_array)
            tweets_list = json.loads(tweets_array)
            return tweets_list
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return []
    else:
        print("No valid JSON array found in the response.")
        return []
    

def process_tweet(tweet):
    # print("test_post_data: "+ tweet)
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret_key = os.getenv('TWITTER_API_SECRET_KEY')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

    if not api_key or not api_secret_key or not access_token or not access_token_secret or not bearer_token:
      raise ValueError("twitter key/secret is not set.")

    # Initialize Tweepy Client for API v2
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret_key,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    tweet_params = {"text": tweet}

    try:
        # Send tweet
        response = client.create_tweet(**tweet_params)
        print("Tweet posted successfully!", response.data)
        return response
    except Exception as e:
        print("Error during tweeting:", e)
        return e


# Create Agents
trending_topic_researcher_agent = agents.trending_topic_researcher_agent()
content_researcher_agent = agents.content_researcher_agent()
creative_agent = agents.creative_content_creator_agent()

# Create Tasks
topic_analysis = tasks.topic_analysis(trending_topic_researcher_agent, niche)
content_research = tasks.content_research(content_researcher_agent, niche)
twitter_posts = tasks.create_twitter_posts(creative_agent, niche)

# Create Crew
crew = Crew(
	agents=[
		trending_topic_researcher_agent,
		content_researcher_agent,
		creative_agent
	],
	tasks=[
		topic_analysis,
		content_research,
		twitter_posts
	],
    process=Process.sequential,
	verbose=True
)

result = crew.kickoff()

print("Crew usage", crew.usage_metrics)

# Print results
print("\n\n########################")
print("## Here is the result")
print("########################\n")
print(result)


tweets = get_tweets_from_llm(result)
print("tweets: ")
print(tweets)

# Process each tweet
for tweet in tweets:
    print(tweet)
    process_tweet(tweet)