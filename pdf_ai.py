import os
import numpy as np
import faiss

from pypdf import PdfReader
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

documents = []

manuals_folder = "manuals"

for filename in os.listdir(manuals_folder):

    if filename.endswith(".pdf"):

        path = os.path.join(manuals_folder, filename)

        reader = PdfReader(path)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

        chunks = text.split("\n\n")

        for chunk in chunks:

            if len(chunk.strip()) > 50:
                documents.append(chunk)

embeddings = []

for doc in documents:

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=doc
    )

    embeddings.append(response.data[0].embedding)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("PDF AI Database Ready")


def ask_pdf(question):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    question_embedding = np.array(
        [response.data[0].embedding]
    ).astype("float32")

    D, I = index.search(question_embedding, k=3)

    context = ""

    for idx in I[0]:

        context += documents[idx] + "\n"

    prompt = f"""
You are an AI manual assistant.

Use the manual information below to answer.

Manual:
{context}

Question:
{question}
"""

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