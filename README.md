# Real-Time Multilingual Query Handler

A simple **AI-powered system** that lets users ask questions in **multiple languages** and receive answers in the **same language**.

The system automatically:
- Detects the user’s language
- Translates the question to English
- Searches a knowledge base
- Generates an answer using an AI model
- Translates the answer back to the user’s language

This project is built mainly for **learning, experimentation, and demonstration**.

---

## What this project does

- Accepts questions in many languages (Spanish, French, Hindi, Chinese, Arabic, etc.)
- Automatically detects and translates the language
- Searches stored documents to find relevant information
- Generates AI-based answers
- Shows results through a simple web interface

---

## Main features

- Multilingual question support
- AI-powered question answering
- Retrieval-Augmented Generation (RAG)
- Simple Streamlit web interface
- Modular and easy-to-understand Python code

---

## Project structure (simplified)

multilingual-query-handler/
├── data/ # Input documents
├── src/ # Core logic (translation, search, AI)
├── ui/ # Streamlit web app
├── main.py # Builds the knowledge base
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## How it works (high level)

1. User enters a question in any language
2. System detects and translates the language
3. Relevant documents are retrieved from the knowledge base
4. AI generates an answer
5. Answer is translated back to the user’s language
6. Result is shown in the web interface

> Internal implementation details are kept simple and modular.

<img width="1919" height="933" alt="image" src="https://github.com/user-attachments/assets/bbdcc7bf-6dd4-41af-9cad-dc45bfd1d81b" />

---

## Running the demo (basic steps)

1. Create a Python virtual environment (Python 3.10 recommended)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Add your API keys as environment variables (do not commit them)
4. Build the knowledge base:
  python main.py

6. Start the web app:
  streamlit run ui/app.py

7. Open the local URL shown in the terminal

## Configuration notes

API keys are read from environment variables
No secrets are stored in the repositor
The system can work with different AI models and document sources

## Security & privacy

1. Do not commit API keys or credentials
2. Do not upload real personal data
3. Use environment variables for all sensitive information



## Thank you for checking out this project!


---
