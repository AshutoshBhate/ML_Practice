import os
from openai import OpenAI

# The client will automatically look for the OPENAI_API_KEY environment variable.
# Make sure you have set it up as shown in the next section.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

try:
    response = client.chat.completions.create(
        # Using a real model name like gpt-3.5-turbo. "gpt-5-nano" doesn't exist.
        model="gpt-5-nano",
        # The input is passed as a list of messages.
        messages=[
            {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
        ]
    )

    # The response text is located in choices[0].message.content
    print(response.choices[0].message.content)

except Exception as e:
    print(f"An error occurred: {e}")