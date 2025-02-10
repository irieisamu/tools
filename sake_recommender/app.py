from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    option1 = request.form.get('option1', 'なし')
    option2 = request.form.get('option2', 'なし')
    result = f'グループ1の選択: {option1}, グループ2の選択: {option2}'
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
