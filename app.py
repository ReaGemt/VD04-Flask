from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Необходим для использования flash-сообщений

# Логирование
logging.basicConfig(filename='app.log', level=logging.INFO)


def send_email(name, email, message):
    """Отправка письма с данными формы"""
    msg = MIMEText(f'Сообщение от {name} ({email}):\n\n{message}')
    msg['Subject'] = 'Новое сообщение с сайта'
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'your_email@example.com'

    with smtplib.SMTP('smtp.example.com') as server:
        server.login('your_email@example.com', 'your_password')
        server.send_message(msg)


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

        # Проверка данных формы
        if not name or not email or not message:
            flash('Все поля обязательны для заполнения.', 'error')
            return redirect(url_for('contacts'))

        # Валидация email с помощью reCAPTCHA или JavaScript
        if "@" not in email:
            flash('Пожалуйста, введите корректный адрес электронной почты.', 'error')
            return redirect(url_for('contacts'))

        # Отправка письма и логирование
        send_email(name, email, message)
        logging.info(f'Сообщение отправлено от {name} ({email})')

        flash(f'Спасибо за ваше сообщение, {name}!', 'success')
        return redirect(url_for('contacts'))
    return render_template('contacts.html')


# Страница "О нас"
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)  # Важно: убедитесь, что здесь стоит debug=True
