from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    selection = request.form['option']
    return jsonify({'result': f'あなたの選択: {selection}'})

if __name__ == '__main__':
    app.run(debug=True)
