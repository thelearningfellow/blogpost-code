from openai import OpenAI

client = OpenAI(
    api_key="dummy_value", base_url="http://localhost:12434/engines/llama.cpp/v1"
)

response = client.embeddings.create(
    model="ai/mxbai-embed-large",
    input=["Please write 500 words about the fall of Rome."],
)

print(response.data[0].embedding)
