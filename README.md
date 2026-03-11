# An intelligent AI sales agent

</div>

## 📖 Overview

The Sales AI Agent is a conversational AI system engineered to act as an automated sales representative for electronic stores. Leveraging large language models and agentic frameworks, it automates customer interactions, provides detailed product information, and streamlines the sales process. This agent aims to improve customer experience, increase engagement, and assist in driving sales by providing instant, accurate, and context-aware support.

## ✨ Features

-   🎯 **Intelligent Sales Conversations**: Engage customers in natural, human-like dialogues about products and purchasing.
-   📚 **Product Knowledge Integration**: Access and retrieve specific product information from a dedicated knowledge base (`data/`).
-   💬 **Contextual Understanding**: Maintain conversational context across interactions to provide relevant and coherent responses.
-   💾 **Chat History Management**: Store and retrieve past conversation data for continuous and personalized user experiences (`chats/`).
-   🛍️ **Personalized Recommendations**: Suggest suitable products based on customer queries, preferences, and browsing history.
-   🚀 **Automated Support**: Handle common sales inquiries and guide users through potential purchase paths efficiently.

## 🛠️ Tech Stack

**Core AI & Backend:**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

![LangChain](https://img.shields.io/badge/LangChain-0.1.0-blue?style=for-the-badge&logo=langchain&logoColor=white)

![OpenAI](https://img.shields.io/badge/OpenAI-FF9900?style=for-the-badge&logo=openai&logoColor=white)

![python-dotenv](https://img.shields.io/badge/python--dotenv-v1.0.0-informational?style=for-the-badge)

## 🚀 Quick Start

Follow these steps to set up and run the Sales AI Agent locally.

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/angelmdezhdez/sales-ai-agent.git
    cd sales-ai-agent
    ```

2.  **Install dependencies**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    If a `requirements.txt` file is present (check the repository root), install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    Otherwise, you may need to install core dependencies manually:
    ```bash
    pip install langchain google-genai python-dotenv chromadb
    ```

3.  **Environment setup**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```bash
    cp .env.example .env # If .env.example exists, otherwise create .env
    ```
    Open `.env` and configure your environment variables:
    ```
    GOOGLE_GEMINI_API_KEY="your_openai_api_key_here"
    # Add other environment variables as detected or needed
    ```

4.  **Data preparation**
    Populate the `data/` directory with your product information or knowledge base files as needed for the agent to function effectively. This might involve text files, CSVs, or other formats that can be processed into a vector store.

5.  **Run the AI agent**
    ```bash
    python main.py
    ```
    The agent should start, and you can interact with it through the console.

## 📁 Project Structure

```
sales-ai-agent/
├── agent/             # Core AI agent logic, tools, and prompts
├── chats/             # Stores chat history and interaction logs
├── data/              # Product information, knowledge base, or training data
├── utils/             # Reusable helper functions and utilities
├── .gitignore         # Specifies intentionally untracked files to ignore
├── LICENSE            # MIT License file
├── main.py            # Main entry point for the AI sales agent
└── README.md          # Project README (this file)
```

## 🗣️ Agent Interaction

To interact with the sales agent, simply run `main.py` as described in the [Run the AI agent](#5-run-the-ai-agent) section. The agent will typically provide a prompt in your console where you can type your queries or sales-related questions.

```bash

# Example interaction:
python main.py
> Agent: Hello! Welcome to our electronics store. How can I assist you today?
> User: I'm looking for a new laptop for gaming.
> Agent: Great! We have a wide range of gaming laptops. Are you looking for something specific, like a certain brand or price range?

# ... and so on.
```


## 🙏 Acknowledgments

-   Built using **LangChain** for robust agent orchestration.
-   Powered by **Google GenAI**'s cutting-edge language models.
-   Inspired by the growing field of AI-driven customer service and sales automation.

