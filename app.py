import os
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="AI Email Generator", page_icon="✉️", layout="centered")

st.title("✉️ AI Email Generator")
st.write("Generate professional emails in seconds using Groq & Meta Llama 3.3.")

# Retrieve API key from environment variables or Streamlit secrets
groq_api_key = os.environ.get("GROQ_API_KEY")

# Fallback sidebar input if environment variable/secrets aren't configured yet
if not groq_api_key:
    groq_api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
    st.sidebar.markdown("[Get a free Groq API Key](https://console.groq.com/keys)")

# User Inputs
recipient = st.text_input("Recipient (e.g., Hiring Manager, Client, Boss):")
topic = st.text_area("Email Purpose / Key Details:", placeholder="Briefly describe what the email should be about...")

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Tone:", ["Professional", "Friendly", "Persuasive", "Formal", "Urgent"])
with col2:
    length = st.selectbox("Length:", ["Short", "Medium", "Detailed"])

# Generation Logic
if st.button("Generate Email", type="primary"):
    if not groq_api_key:
        st.error("Please provide a valid Groq API key to generate emails.")
    elif not topic.strip():
        st.warning("Please provide the purpose or details for the email.")
    else:
        try:
            client = Groq(api_key=groq_api_key)
            
            prompt = f"""
            Write an email based on the following details:
            - Recipient: {recipient if recipient else 'General'}
            - Purpose/Details: {topic}
            - Tone: {tone}
            - Length: {length}

            Format: Include a subject line clearly labeled as 'Subject:' at the top, followed by the email body.
            """

            with st.spinner("Generating your email..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": "You are an expert email generator."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                )

            email_content = response.choices[0].message.content

            st.success("Email Generated!")
            st.text_area("Generated Email:", value=email_content, height=300)
            st.code(email_content, language="markdown")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
