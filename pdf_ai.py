import os
import faiss
import numpy as np

from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# OPENAI API

import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# AI MODEL

model = SentenceTransformer("all-MiniLM-L6-v2")

# STORE PDF TEXT

all_text = []

manuals_folder = "manuals"

# READ ALL PDF FILES AUTOMATICALLY

for file in os.listdir(manuals_folder):

    if file.endswith(".pdf"):

        path = os.path.join(manuals_folder, file)

        reader = PdfReader(path)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        # SPLIT TEXT INTO CHUNKS

        chunks = text.split(". ")

        all_text.extend(chunks)

# CREATE EMBEDDINGS

embeddings = model.encode(all_text)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

print("PDF AI Database Ready")

# FORMAT RESPONSE

def format_answer(answer):

    answer = answer.replace("1.", "\n1.")
    answer = answer.replace("2.", "\n2.")
    answer = answer.replace("3.", "\n3.")
    answer = answer.replace("4.", "\n4.")
    answer = answer.replace("5.", "\n5.")

    return answer.strip()

# MAIN AI FUNCTION

def ask_pdf(question):

    # SEARCH PDF

    question_embedding = model.encode([question])

    D, I = index.search(np.array(question_embedding), k=3)

    results = []

    for i in I[0]:

        results.append(all_text[i])

    context = "\n".join(results)

    # OPENAI RESPONSE

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",
                "content": """
                You are a professional AI Manual Assistant.

                Rules:
                - Answer clearly
                - Make answers short and clean
                - Use bullet points when needed
                - If user asks "make it short" then shorten
                - If user asks "easy" explain simply
                - Always answer in English
                - Organize answers professionally
                """
            },

            {
                "role": "user",
                "content": f"""
                Manual Content:
                {context}

                User Question:
                {question}
                """
            }

        ]

    )

    answer = response.choices[0].message.content

    answer = format_answer(answer)

    return answer