from server import server
from chatgpt import gpt

def on_user_message(text, socketio):
    try:
        reply = gpt(text)           
    except Exception as e:
        reply = f"伺服器錯誤：{e}"
    print(f"GPT replies: {reply}")
    socketio.emit('message', reply, to=None, namespace='/')

app, socketio = server(on_user_message)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=80)