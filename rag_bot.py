#Task 2.3

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

load_dotenv()

DOCS_FOLDER = "docs"


def load_documents(folder_path: str):
    documents = []

    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return documents

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, file_name)
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            for doc in docs:
                doc.metadata["source_file"] = file_name

            documents.extend(docs)

    return documents


def build_vectorstore(documents):
    splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.from_documents(split_docs, embeddings)


def ask_question(vectorstore, question: str):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(question)

    if not docs:
        return {
            "answer": "I cannot answer that because it is outside the provided documents.",
            "source": None,
            "quote": None
        }

    context = "\n\n".join(doc.page_content for doc in docs)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = f"""
You are a document-grounded assistant.

Answer the user's question using ONLY the context below.
If the answer is not supported by the context, reply exactly:
I cannot answer that because it is outside the provided documents.

Question:
{question}

Context:
{context}
"""

    response = llm.invoke(prompt)
    top_doc = docs[0]

    return {
        "answer": response.content.strip(),
        "source": top_doc.metadata.get("source_file", "Unknown source"),
        "quote": top_doc.page_content[:250].replace("\n", " ")
    }


def main():
    documents = load_documents(DOCS_FOLDER)

    if not documents:
        print("No PDF documents found in the docs folder.")
        return

    vectorstore = build_vectorstore(documents)

    print("RAG bot ready. Type 'exit' to quit.\n")

    while True:
        question = input("Ask something: ").strip()

        if question.lower() == "exit":
            break

        result = ask_question(vectorstore, question)

        print("\nAnswer:", result["answer"])
        print("Source:", result["source"])
        print("Quote:", result["quote"])
        print("-" * 80)


if __name__ == "__main__":
    main()