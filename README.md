# AI News Reporter

## Overview
AI News Reporter is an AI-powered application that fetches and summarizes the latest news articles on artificial intelligence and related topics. Users can enter a topic and specify the number of articles to retrieve, and the system will provide concise LinkedIn-style summaries using advanced language models.

## Features
- **Real-time AI News Fetching:** Retrieves the latest AI-related news using SerpAPI.
- **Automated Summarization:** Summarizes news articles using Groq’s LLaMA 3 model.
- **Dynamic Input Options:** Users can specify topics and the number of articles.
- **User-friendly Interface:** Built with Gradio for easy interaction.

## Technologies Used
- **Python**: Core programming language
- **Gradio**: For the web-based UI
- **Groq API**: To generate AI-powered summaries
- **SerpAPI**: To fetch the latest news articles
- **Google Colab**: For authentication and cloud execution
- **Vertex AI (Gemini 1.5 Pro)**: For additional content generation

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Pip package manager
- API keys for SerpAPI and Groq (stored in Google Colab user data)

### Installation
Clone the repository:
```sh
git clone https://github.com/yourusername/ai-news-reporter.git
cd ai-news-reporter
```
Install dependencies:
```sh
pip install gradio groq requests beautifulsoup4 vertexai
```

## Usage
Run the application:
```sh
python app.py
```
Alternatively, launch it in Google Colab.

### How to Use
1. Enter a topic in the provided text field.
2. Select the number of news articles to retrieve using the slider.
3. Click the submit button to generate summaries.

## Example Output
**Input:** "Generative AI"

**Output:**
- **Title:** OpenAI Introduces GPT-5
- **Date Published:** March 2025
- **Summary:** OpenAI has unveiled GPT-5, bringing new advancements in reasoning and multimodal capabilities...

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit changes.
4. Open a pull request.

## License
This project is licensed under the MIT License.

## Contact
For inquiries or feedback, reach out via [your.email@example.com](mailto:your.email@example.com) or open an issue on GitHub.

