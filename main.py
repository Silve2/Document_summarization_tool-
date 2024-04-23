import json
import requests
import streamlit as st
import os
import pdfplumber

api_key = 'YOUR_API_KEY'


def save_uploaded_file(uploaded_file):
    try:
        os.makedirs('uploaded_files', exist_ok=True)
        file_path = os.path.join('uploaded_files', uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:

        return str(e)


def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


def summarize_text(file_path):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user",
             "content": f"Riassumi questo testo su una riga mettendo Riassunto: e su un'altra metti un probabile titolo"
                        f", Titolo: "
                        f"{extract_text_from_pdf(file_path)}"}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    responseText = json.loads(response.content)['choices'][0]['message']['content']
    json_response = json.loads(response.content)['choices'][0]

    start = responseText.find('Riassunto:') + len("Riassunto: ")
    end = responseText.find("Titolo:")
    summary = responseText[start:end]
    start = end + len("Titolo: ")
    end = responseText.find("#!#!")
    title = responseText[start:end]

    return summary, title, json_response


def write_text(summary, title, jsonResp):
    col1, col2 = st.columns(2)

    with col1:
        st.header("Title")
        st.write(title)
    with col2:
        st.header("Summary")
        st.write(summary)

    st.header("JSON response")
    st.markdown("""
        <style>
        .stCodeBlock {
            overflow-x: auto;  
            white-space: pre-wrap;  
            word-break: break-word;  
            max-width: 90%;  
            min-height: 500px;
        }
        </style>
        """, unsafe_allow_html=True)
    json_data = json.dumps(jsonResp, indent=4)
    st.code(json_data, language='json')


st.title('Inserisci un file, ti verrà fornito un riassunto e un suggerimento per un titolo da dare al documento')

uploaded_file = st.file_uploader("Scegli un file", type=['pdf'])

if uploaded_file is not None:

    file_type = uploaded_file.type
    st.write('Tipo di file:', file_type)

    if file_type == 'application/pdf':

        file_path = save_uploaded_file(uploaded_file)
        summary, title, jsonResp = summarize_text(file_path)
        write_text(summary, title, jsonResp)

    else:
        st.error("Formato file non supportato!")
