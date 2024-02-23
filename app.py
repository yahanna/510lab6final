from tempfile import NamedTemporaryFile
import os
import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Resume Chat & Feedback",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about your document or upload your resume for feedback!"}
    ]

def extract_resume_data(pdf_path):
    # 假设的简历解析逻辑，基于新的简历模板
    resume_data = {
        "name": "Ronald Bandell",
        "email": "ronaldbandell@email.com",
        "summary": "Highly motivated professional with over seven years of experience managing technology-based projects. Certified Associate in Project Management (CAPM).",
        "skills": [
            "Project setup, monitoring and coordination",
            "Strategy formulation and execution",
            "System analysis and design",
            "Word processing and presentation software"
        ],
        "professional_experience": [
            {
                "position": "Senior Administrative Assistant",
                "company": "Hugh Consulting, Inc.",
                "years": 5,  # 从2015到现在
                "achievements": [
                    "Streamline the company’s project management system",
                    "Conduct training for staff on document versioning"
                ]
            },
            {
                "position": "Administrative Assistant",
                "company": "Hitech Project Solutions, LLC",
                "years": 4,  # 从2007到2011
                "achievements": [
                    "Streamlined the process for proposal development",
                    "Developed and implemented a client tracking system"
                ]
            }
        ],
        "certifications": [
            "Certified Associate in Project Management (CAPM)",
            "Microsoft Certified Solutions Developer (MCSD) – SharePoint"
        ],
        "education": "Master of Business Administration, University of Dallas, 2005",
        "associations": [
            "Project Management Institute",
            "American Management Association"
        ]
    }
    return resume_data


def generate_feedback(resume_data):
    feedback_list = []
    
    # summary
    if "seven years" in resume_data["summary"]:
        feedback_list.append("Great job highlighting your extensive experience in your summary.")
    
    # skills
    if len(resume_data["skills"]) < 5:
        feedback_list.append("Your skills section is concise and relevant. Consider adding more specific skills if applicable.")
    
    # work experience
    total_years_experience = sum(item["years"] for item in resume_data["professional_experience"])
    if total_years_experience < 10:
        feedback_list.append("You have a solid foundation of professional experience. Highlighting more achievements could provide a clearer picture of your capabilities.")
    else: 
        feedback_list.append("You professional experience seems not so effiency, you can add more bussiness or intern experience")
    
    # certifications
        
    if "CAPM" in resume_data["certifications"][0]:
        feedback_list.append("Your CAPM certification is a strong asset. Make sure it's prominently displayed.")
    if "Figma" in resume_data["certifications"][0]:
        feedback_list.append("Your design certification is a strong asset. Make sure it's prominently displayed.")\
        
    # education
    if "Master of Business Administration" in resume_data["education"]:
        feedback_list.append("Your advanced degree in business administration is impressive. Ensure it's clearly highlighted.")
    
    # general
    if not feedback_list:  # 如果没有具体反馈
        feedback = "Your resume is well-organized and highlights your qualifications effectively. Ensure it's tailored to the job you're applying for."
    else:
        feedback = "Here are some suggestions for your resume:\n- " + "\n- ".join(feedback_list)
    
    return feedback



uploaded_file = st.file_uploader("Upload your document or resume")

if uploaded_file:
    bytes_data = uploaded_file.read()
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(bytes_data)
        tmp_path = tmp.name
        reader = PDFReader()
        docs = reader.load_data(tmp_path)
        llm = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
            model="gpt-3.5-turbo",
            temperature=0.0,
            system_prompt="You are an expert on the content of the document, provide detailed answers to the questions. Use the document to support your answers.",
        )
        index = VectorStoreIndex.from_documents(docs)
    os.remove(tmp_path)  # remove temp file
    
    if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="condense_question", verbose=False, llm=llm
        )
    
    # Generate and display feedback for resumes
    if uploaded_file.type == "application/pdf":  # Check if the uploaded file is a PDF
        resume_data = extract_resume_data(tmp_path)
        feedback = generate_feedback(resume_data)
        st.session_state.messages.append({"role": "assistant", "content": feedback})  # Display feedback as a message

if prompt := st.chat_input("Your question or upload your resume for feedback"):  # Prompt for user input
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.stream_chat(prompt)
            st.write_stream(response.response_gen)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history
