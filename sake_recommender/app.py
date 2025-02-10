from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# OpenAI APIキーを環境変数から取得
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    sake_type = request.form.get('option1', 'なし')
    sake_taste = request.form.get('option2', 'なし')

    # ChatGPT APIにリクエストを送信
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは日本酒の専門家です。ユーザーの好みに合わせて日本酒を3本推薦してください。"},
            {"role": "user", "content": f"日本酒の種類: {sake_type}, 味: {sake_taste}のおすすめの日本酒を3本教えてください。それぞれの日本酒について、名前と簡単な説明を提供してください。"}
        ]
    )

    # ChatGPTの回答を取得
    recommendations = response.choices[0].message.content

    result = f'選択された条件: {sake_type}（{sake_taste}）\n\nおすすめの日本酒:\n{recommendations}'
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
