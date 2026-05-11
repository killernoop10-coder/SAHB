from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

documents = []

folder_path = "manuals"

for filename in os.listdir(folder_path):

    if filename.endswith(".pdf"):

        pdf_path = os.path.join(folder_path, filename)

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text()

        chunks = text.split('.')

        for chunk in chunks:

            if len(chunk.strip()) > 20:
                documents.append(chunk.strip())

embeddings = model.encode(documents)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

print("PDF AI Database Ready")

while True:

    query = input("Ask: ")

    query_embedding = model.encode([query])

    D, I = index.search(np.array(query_embedding), k=1)

    print("\nAnswer:\n")

    print(documents[I[0][0]])

    print("\n")