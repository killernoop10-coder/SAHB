import os
import numpy as np
import faiss

from pypdf import PdfReader
from openai import OpenAI

# OPENAI API
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

documents = []

manuals_folder = "manuals"

# READ ALL PDF FILES
for filename in os.listdir(manuals_folder):

    if filename.endswith(".pdf"):

        path = os.path.join(manuals_folder, filename)

        print(f"Reading PDF: {filename}")

        reader = PdfReader(path)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

        # SPLIT TEXT INTO SMALL CHUNKS
        chunks = []

        chunk_size = 1000

        for i in range(0, len(text), chunk_size):

            chunks.append(text[i:i + chunk_size])

        # SAVE CHUNKS
        for chunk in chunks:

            if len(chunk.strip()) > 100:

                documents.append(chunk)

print("Creating AI Database...")

# CREATE EMBEDDINGS
embeddings = []

for doc in documents:

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=doc
    )

    embeddings.append(response.data[0].embedding)

embeddings = np.array(embeddings).astype("float32")

# CREATE FAISS INDEX
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("PDF AI Database Ready")


def ask_pdf(question):

    # QUESTION EMBEDDING
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    question_embedding = np.array(
        [response.data[0].embedding]
    ).astype("float32")

    # SEARCH
    D, I = index.search(question_embedding, k=3)

    context = ""

    for idx in I[0]:

        context += documents[idx] + "\n"

    # LIMIT CONTEXT SIZE
    context = context[:4000]

    # PROMPT
    prompt = f"""
You are a professional AI manual assistant.

Answer using ONLY the manual information below.

Manual Information:
{context}

Question:
{question}

Answer clearly and professionally.
"""

    # GPT RESPONSE
    answer = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return answer.choices[0].message.content