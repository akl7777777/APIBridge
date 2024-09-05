from openai import OpenAI

client = OpenAI(api_key="sk-xxx", base_url="http://127.0.0.1:5566/snova/v1")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    stream=True,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

for chunk in completion:
    print(chunk.choices[0].delta)