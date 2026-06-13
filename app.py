from flask import Flask, render_template # Импортируем рендеринг шаблонов

app = Flask(__name__)

@app.route('/')
def home():
    # Flask сам пойдёт в папку templates, найдёт файл index.html и покажет его в браузере
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)