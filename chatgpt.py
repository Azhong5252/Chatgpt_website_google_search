from openai import OpenAI
import requests

import tiktoken 
TOKEN_LIMIT   = 8000          
TOKEN_MARGIN  = 500         
enc = tiktoken.encoding_for_model("gpt-4o-mini")


messages = [{"role": "system", "content": "你是一個知識豐富的助理。"}]
use_search = False

def gpt(question):
    global messages
    global use_search

    client = OpenAI(api_key="")
    GOOGLE_API_KEY = ""
    GOOGLE_CX = ""

    def trim_if_needed():
        total = sum(len(enc.encode(m["content"])) for m in messages)
        while total > TOKEN_LIMIT - TOKEN_MARGIN and len(messages) > 2:
            del messages[1:3]                
            total = sum(len(enc.encode(m["content"])) for m in messages)


    def google_search(query):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CX,
            "q": query,
            "num": 3
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        results = []
        for item in data.get("items", []):
            title = item.get("title")
            snippet = item.get("snippet")
            link = item.get("link")
            results.append(f"{title}\n{snippet}\n{link}")
        return "\n\n".join(results)

    def gpt_answer_with_search(question):
        global use_search

        if question == "search":
            use_search = True
            return "已開啟搜尋模式"
        elif question == "not search":
            use_search = False
            return "已關閉搜尋模式"

        if use_search:
            search_results = google_search(question)
            prompt = (
                "請根據以下的網路搜尋結果回答問題，並用繁體中文回答：\n\n"
                f"{search_results}\n\n"
                f"問題：{question}"
            )
        else:
            prompt = f"使用繁體中文回答：{question}"

        messages.append({"role": "user", "content": prompt})

        trim_if_needed()  

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=200,
            temperature=0.7,
        )

        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply

    answer = gpt_answer_with_search(question)
    return answer

if __name__ == "__main__":
    while True:
        question = input("請輸入文字：")
        answer = gpt(question)
        print("GPT 回答：", answer)