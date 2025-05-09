from openai import OpenAI

client = OpenAI(
    api_key="dummy_value",
    base_url="http://localhost:12434/engines/llama.cpp/v1"
)

response = client.chat.completions.create(
    model="ai/smollm2",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)

print(response.choices[0].message.content)