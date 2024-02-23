# Lab 6 - Chat with PDF

## Getting Started

1. `python -m venv venv`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`
1. `cp .env.sample .env`
1. Change the `.env` file to match your environment
1. `streamlit run app.py`


# AI Resume Feedback and Document Chatbot

This project presents an innovative AI Resume Feedback and Document Chatbot, designed to provide instant feedback on resumes and facilitate interactive document-based Q&A sessions. Leveraging cutting-edge AI technologies, this chatbot aims to assist users in refining their resumes for better job prospects while enabling them to ask detailed questions about any document they upload, including but not limited to resumes.

## Features

- **Resume Feedback**: Upload your resume in PDF format to receive tailored feedback aimed at improving your presentation and content, enhancing your chances of landing job interviews.
- **Document Chat**: Engage in a conversational Q&A session with the chatbot about the content of any uploaded document, making it easier to extract and understand information quickly.
- **AI-Powered Insights**: Utilizes OpenAI's advanced language models to analyze resumes and documents, ensuring feedback and responses are insightful and relevant.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or newer
- Pip for Python package installation

### Installation

1. Clone the repository to your local machine:
    ```sh
    git clone https://github.com/your-username/ai-resume-feedback-chatbot.git
    ```

2. Navigate to the project directory:
    ```sh
    cd ai-resume-feedback-chatbot
    ```

3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables for OpenAI API access by creating a `.env` file in the project root with the following content:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

### Running the Application

To start the application, run the following command in the terminal:
```sh
streamlit run app.py
