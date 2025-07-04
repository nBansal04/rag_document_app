import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(user_query, vector_store):
    results = vector_store.similarity_search(user_query, k=4)

    context = "\n\n\n".join([
        f"Page Content: {doc.page_content}\nPage Number: {doc.metadata.get('page_label') or doc.metadata.get('page')}"
        for doc in results
    ])

    SYSTEM_PROMPT = f"""
    You are a helpful assistant. Use only the following PDF context to answer the user's question.
    If you can't find the answer, say so politely.

    Context:
    {context}
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ]
    )

    return response.choices[0].message.content
