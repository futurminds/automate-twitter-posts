# Automate Twitter with LLaMA 3 and CrewAI

Welcome to the **Automate Twitter with LLaMA 3 and CrewAI** project! This project leverages the power of AI to create and post tweets automatically based on trending topics and detailed research. You can set this up on your local machine using tools from Groq Cloud and CrewAI.

## Overview

This application uses a combination of tools to automate the process of finding trending topics, researching them, crafting tweets, and posting them on Twitter. The main components are:

- **Tools**: BrowserTool, SearchTool, and TrendsTool for gathering and processing data.
- **Agents**: Virtual assistants that use the tools to perform specific tasks.
- **Tasks**: Defined actions that agents need to complete.
- **Crew**: The overall process that combines agents and tasks to achieve the goal.

## Features

- **Trending Topic Research**: Identifies current trending topics using Google Trends.
- **Content Research**: Conducts in-depth research on trending topics.
- **Twitter Content Creation**: Crafts engaging tweets based on researched content.
- **Automated Posting**: Posts the generated tweets to Twitter.

## Setup Instructions

### Prerequisites

- Python 3.8+
- [Groq API Key](https://groq.com/)
- [Twitter Developer Account](https://developer.twitter.com/)
- [Serper API Key](https://serper.dev/)
- .env file with the following variables:
  - `MODEL`
  - `GROQ_API_KEY`
  - `TWITTER_API_KEY`
  - `TWITTER_API_SECRET_KEY`
  - `TWITTER_ACCESS_TOKEN`
  - `TWITTER_ACCESS_TOKEN_SECRET`
  - `TWITTER_BEARER_TOKEN`
  - `SERPER_API_KEY`

### Installation

1. **Clone the Repository**

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add the necessary environment variables:

   ```
   MODEL=your_model
   GROQ_API_KEY=your_groq_api_key
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET_KEY=your_twitter_api_secret_key
   TWITTER_ACCESS_TOKEN=your_twitter_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
   TWITTER_BEARER_TOKEN=your_twitter_bearer_token
   SERPER_API_KEY=your_serper_api_key
   ```

### Running the Application

1. **Start the Application**

   ```bash
   python main.py
   ```

2. **Follow the Prompts**

   The application will prompt you for your niche and then proceed to create and post tweets based on the research it performs.

## Usage

### Tools

- **BrowserTools**: For scraping web pages and summarizing content using Beautiful Soup.
- **SearchTools**: For performing Google searches using Serper API.
- **TrendsTools**: For fetching trending Google search topics using Pytrends.

### Agents

- **Trending Topic Researcher**: Uses TrendsTools and BrowserTools to identify and compile trending topics.
- **Content Researcher**: Uses BrowserTools and SearchTools to conduct detailed research on topics.
- **Creative Content Creator**: Uses the researched content to craft engaging tweets.

### Tasks

- **Topic Analysis**: Finds and lists trending topics.
- **Content Research**: Gathers detailed information on trending topics.
- **Twitter Posts Creation**: Crafts and prepares tweets for posting.

## Contributing

We welcome contributions! Please fork the repository and create a pull request with your changes.
