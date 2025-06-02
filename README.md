**FAQ Bot - Powered by Langgraph, ChromaDB, and OpenAI**

**Welcome to the FAQ_Bot repository! This project demonstrates how to leverage Generative AI for building a smart frequently asked questions bot using a large language model.**

**Getting Started**
Clone the repository, set up the virtual environment, and install the required packages
1. git clone https://github.com/eric220/FAQ_Bot.git
2. conda create -n your_environment_name python=3.11. conda activate your_environment_name
3. pip install -r requirements.txt

**Store API Keys**
inside the config_files folder, create a config.py file with the text OPENAI_API_KEY=your_openai_api_key.

*Make sure to replace the placeholder your_openai_api_key with your actual key.*

**Add your context**
replace corpus.txt with your answers to frequently asked questions. This bot works best with short answers seperated by an empty line in the .txt file.

**Run the app**
To start the chatbot, run the following command:
streamlit run app.py

**Using the Chatbot**
Once launched, simply ask your questions in the text box:
