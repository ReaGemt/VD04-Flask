from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Необходим для использования flash-сообщений

# Главная страница, отображающая текущие дату и время
@app.route('/')
def home():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', current_time=current_time)

# Страница блога
@app.route('/blog')
def blog():
    return render_template('blog.html')

# Страница контактов с формой обратной связи
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Обработка данных формы (например, отправка по email или сохранение в базу данных)
        flash(f'Спасибо за ваше сообщение, {name}!', 'success')
        return redirect(url_for('contacts'))
    return render_template('contacts.html')

# Страница "О нас"
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
