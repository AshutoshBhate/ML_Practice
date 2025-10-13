import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

try:
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
        ]
    )
    
    print(response.choices[0].message.content)

except Exception as e:
    print(f"An error occurred: {e}")