Self-Improving RAG Content Generator

An AI-powered content generation application built using Python, Google's Gemini API, Retrieval-Augmented Generation (RAG), automated quality evaluation, and memory-based feedback.

The project generates educational content using reference knowledge, evaluates the generated output against predefined quality criteria, and uses evaluation feedback to support continuous improvement.

Project Overview

The Self-Improving RAG Content Generator is designed to improve the quality and reliability of AI-generated educational content.

Instead of relying only on an AI model's general knowledge, the application uses a reference knowledge base to provide supporting context during content generation.

Generated content is then evaluated using a structured evaluation rubric.

Key Features

RAG-based Content Generation: Uses reference material from a knowledge base to provide context for content generation.

Google Gemini Integration: Uses Google's Gemini API for AI-powered content generation.

Automated Content Evaluation: Evaluates generated content against predefined quality criteria.

Memory-Based Feedback: Stores evaluation failures and feedback to support future improvements.

Quality Assessment: Identifies content issues and areas requiring improvement.

Streamlit Interface: Provides an interactive user interface for working with the application.

Python-Based Architecture: Uses modular Python files to separate generation, evaluation, configuration, and memory functionality.

Technology Stack

Technology

Purpose

Python

Core programming language

Google Gemini API

AI content generation

RAG

Reference-based content generation

Streamlit

User interface

JSON

Evaluation rubric and structured data

python-dotenv

Environment variable management

Git and GitHub

Version control and project hosting

Project Structure

self-improving-rag-content-generator/
│
├── app.py
├── main.py
├── config.py
├── generator.py
├── evaluator.py
├── memory.py
├── prompts.py
├── rubric.json
├── requirements.txt
├── README.md
│
├── knowledge_base/
│   └── rag_reference.md
│
├── test_evaluator.py
├── test_failure.py
├── test_memory.py
├── test_self_improvement.py
│
└── .gitignore

Installation and Setup

1. Clone the repository

git clone https://github.com/shivanii112/self-improving-rag-content-generator-Copy.git

2. Navigate to the project directory

cd self-improving-rag-content-generator-Copy

3. Create a virtual environment

python -m venv .venv

4. Activate the virtual environment

For Windows PowerShell:

.venv\Scripts\Activate.ps1

5. Install dependencies

pip install -r requirements.txt

6. Configure the Gemini API key

Create a .env file in the project root directory.

Add your Gemini API key:

GEMINI_API_KEY=your_gemini_api_key_here

Never upload your actual API key to GitHub.

7. Run the application

streamlit run app.py

The Streamlit application will open in your browser.

How the Project Works

Knowledge Base: Loads reference information from the knowledge base.

Content Generation: Sends the topic and supporting context to the Gemini API.

Content Evaluation: Evaluates the generated content using predefined criteria and the evaluation rubric.

Failure Identification: Identifies errors and quality issues in generated content.

Memory Storage: Stores evaluation failures and feedback.

Continuous Improvement: Uses stored feedback to support improvements in subsequent content generation.

Testing

The project includes Python test files for evaluating different components.

Run the tests individually:

python test_evaluator.py

python test_failure.py

python test_memory.py

python test_self_improvement.py

Future Enhancements

Improve retrieval mechanisms for larger knowledge bases.

Introduce advanced RAG evaluation techniques.

Add more detailed performance and quality metrics.

Improve memory-based feedback and learning mechanisms.

Expand support for different educational content formats.

Learning Outcomes

Through this project, I explored:

Python application development.

Retrieval-Augmented Generation (RAG).

Large Language Model (LLM) integration.

Prompt engineering.

Automated AI content evaluation.

Feedback and memory-based improvement.

Streamlit application development.

Git and GitHub version control.

Author

Developed as a hands-on project to explore Generative AI, Python development, RAG systems, and automated AI evaluation.

License

No license has currently been selected for this repository.