# Install required packages
# pip install gradio groq requests beautifulsoup4

import requests
import gradio as gr
from groq import Groq
from bs4 import BeautifulSoup
from google.colab import userdata
from google.colab import auth
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

auth.authenticate_user()

# API Keys
SERP_API_KEY = userdata.get("SERP_API_KEY")
GROQ_API_KEY = userdata.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def get_groq_response(prompt, llm="llama3-70b-8192"):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=llm,
    )
    return chat_completion.choices[0].message.content

def get_urls(query, serp_api_key=SERP_API_KEY):
    params = {"q": query, "tbm": "nws", "location": "United States", "api_key": serp_api_key}
    url = "https://serpapi.com/search.json"
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return [{"title": res.get('title', 'No Title'), "link": res.get('link', 'No Link'), "date_published": res.get('date', 'No Date')} for res in data.get('news_results', [])]
    else:
        return []

def scrape_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return ' '.join(soup.get_text().split()[:1000])
    return None

def summarize_ai_news(query, max_links=5):
    links_dict = get_urls(query, SERP_API_KEY)
    responses = []
    
    if links_dict:
        for count, item in enumerate(links_dict[:max_links]):
            link, title, date_published = item.get('link'), item.get('title', 'No Title'), item.get('date_published', 'No Date')
            if link:
                scraped_text = scrape_text_from_url(link)
                response = get_groq_response(f"""
                You are a journalist covering AI breakthroughs.
                Summarize the article below in a LinkedIn post format.
                
                Title: {title}
                Date Published: {date_published}
                URL: {link}
                Context: {scraped_text}
                Keywords: <Provide top 2-3 keywords>
                Summary: <Summarize in 1-2 concise lines>
                """)
                responses.append(response)
    return "\n\n".join(responses)

def generate_ai_impact_prompt(article_dictionary):
    article_data_str = "\n".join([f"{key}: {str(value)}" for key, value in article_dictionary.items()])
    return f"""
    You are an AI expert analyzing impactful Generative AI articles.
    Select the top 15 based on technology, industry influence, and innovation.
    Ensure they are published within the last week, avoid repetition.
    
    Article Data:
    {article_data_str}
    
    Return in LinkedIn post format:
    
    Title: (title)
    Reason for Selection: (brief explanation)
    Summary: (3-4 line summary)
    Date Published: (date)
    URL: (link)
    """

vertexai.init(project="genai-407700", location="us-central1")
model = GenerativeModel("gemini-1.5-pro-002")

def generate(prompt):
    safety_settings = [
        SafetySetting(SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH, SafetySetting.HarmBlockThreshold.OFF),
        SafetySetting(SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, SafetySetting.HarmBlockThreshold.OFF),
        SafetySetting(SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, SafetySetting.HarmBlockThreshold.OFF),
        SafetySetting(SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT, SafetySetting.HarmBlockThreshold.OFF),
    ]
    
    responses = model.generate_content([prompt], safety_settings=safety_settings, stream=True)
    return "".join([response.text for response in responses])

def summarize_news(query, num_articles):
    return summarize_ai_news(query, max_links=num_articles)

# Gradio UI
demo = gr.Interface(
    fn=summarize_news,
    inputs=[gr.Textbox(label="Enter the topic to fetch the latest news updates"), gr.Slider(minimum=1, maximum=10, step=1, label="Number of articles")],
    outputs=gr.Textbox(label="Summarized News"),
    title="AI_News_REPORTER",
    description="Enter a search query for AI-related news and specify the number of articles to summarize."
)

demo.launch()
