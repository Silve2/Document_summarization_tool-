# Document_summarization_tool-

An AI tool with a Streamlit interface that allows users to upload a document and receive a title suggestion and content summarization as outputs. 


## AI Model ##

In the custom assistant, created in Assistants (OpenAi API platform), <i>gpt-3.5-turbo</i> is set as Model.
This version of gpt is cheap ( Input- $0.50 / 1M tokens Output- $1.50 / 1M tokens) but sufficient to retrieve information about the company, its products, and services from a provided PDF document.
- API Configuration <br>
api_key: A variable that needs to be replaced with a valid OpenAI API key to use the AI model from OpenAI.
## Functions ##
- save_uploaded_file(uploaded_file):
Saves the file uploaded by the user in a uploaded_files folder. Handles exceptions during the file saving and returns the saved file path or an error message.
- extract_text_from_pdf(pdf_path):
Extracts text from a PDF file using pdfplumber. Iterates through each page of the PDF and concatenates the text into a single string.
- summarize_text(file_path):
Sends a request to the OpenAI model, specifying the text extracted from a PDF to generate a summary and a title. The request includes headers for authentication and data formatted in JSON. Parses the response to extract the summary and the title.
```
rl = "https://api.openai.com/v1/chat/completions"
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
```
The content of the question is written in italian and also the response.
The text inside the document can be in an other language.
- write_text(summary, title, jsonResp):
Displays the title and summary in two separate columns in the Streamlit user interface. Also shows the complete JSON response in a formatted code block.

## User Experience ##
The user interface is designed to be intuitive:

Users can upload PDF files through an uploader widget.
Sets up the application title and file upload. Manages the logical flow for file type support, text processing, and result display.
File types are checked to ensure they are PDFs.
Results (document title and summary) are clearly displayed.
The complete JSON response is available for review, useful for developers or anyone interested in seeing the raw data.
