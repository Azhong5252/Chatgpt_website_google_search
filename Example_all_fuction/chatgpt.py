from openai import OpenAI
client = OpenAI(api_key = "")

messages = []
def gpt(message):
    messages.append({"role": "user", "content": message})

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=50,
        temperature=0.9
    )
    
    reply = chat_completion.choices[0].message.content 
    messages.append({"role": "assistant", "content": reply})
    return reply
if __name__ == "__main__":
    gpt()