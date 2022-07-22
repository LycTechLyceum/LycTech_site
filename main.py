from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from validate_email import validate_email  # для проверки имейла на существование и корректность
import requests
mn = Blueprint('main_pages', __name__)


@mn.route('/')  # лавная страница
def index():
    if 'login' in session:  # if LOGIN in session - login it without questions
        return redirect(url_for('main_pages.logged'))
    return render_template('main.html')


@mn.route('/logged')
def logged():
    # получаем информацию о пользователе по логину в сессии
    name = "Tim"
    surname = "Smirnov"
    user = {"initials": name + " " + surname}

    return render_template('main-after-login.html', user=user)


@mn.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            if username == 'lol' and password == 'lol':  # проверяем логин и пароль
                # получаем данные о пользователе по логину и отправляем его на страницу
                name = "Tim"
                surname = "Smirnov"
                user = {"initials": name + " " + surname}
                session.clear()
                session['login'] = 'login'
                return render_template("main-after-login.html", user=user)
        flash(error)

    return render_template('login.html')


@mn.route('/signup', methods=('GET', 'POST'))
def signup():  # получаем все, все, все данные :)
    if request.method == 'POST':
        name = str(request.form['username'])
        surname = str(request.form['surname'])
        grade = str(request.form['grade'])
        organisation = str(request.form['organisation'])
        username = str(request.form['login'])
        password = str(request.form['password'])
        error = None

        if not name:
            error = "Name is required."
        elif not surname:
            error = "Surname is required."
        elif not organisation:
            error = "Organisation is required."
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not grade:
            error = "Class is required."

        if error is None:
            user = requests.post('https://db-proglyc-hse.herokuapp.com/api/post-user',
                                      json={"name": name, "surname": surname, "grade": grade, "id_pos": 1})
            print(user)
            return redirect(url_for('main_pages.login'))

        flash(error)
    return render_template('register.html')


@mn.route('/logout')  # чистим сессию и переходим на страницу без регистрации
def logout():
    session.clear()
    return redirect(url_for('main_pages.index'))


@mn.route('/practicum')  # чистим сессию и переходим на страницу без регистрации
def practicum():
    # получаем данные о пользователе по логину и отправляем его на страницу
    name = "Tim"
    surname = "Smirnov"
    user = {"initials": name + " " + surname}
    practices = [{"name": "First", "date": "10.03.2022"}, {"name": "Second", "date": "10.04.2022"}, {"name": "Second", "date": "10.05.2022"}]
    return render_template('practicum.html', user=user, practices=practices)


@mn.route('/reg-to-practicum', methods=('GET', 'POST'))  # чистим сессию и переходим на страницу без регистрации
def reg_to_practicum():
    name = "Tim"
    surname = "Smirnov"
    user = {"initials": name + " " + surname}

    if request.method == 'POST':
        email = request.form['email']
        if validate_email(email, verify=True):  # проверка имейла на валидность (существование или корректность)
            return redirect(url_for('main_pages.email_is_valid'))
        else:
            error = "Ваш имейл некорректен"
            flash(error)
    return render_template('reg-to-practicum.html', user=user)


@mn.route('/email-is-valid')  # чистим сессию и переходим на страницу без регистрации
def email_is_valid():
    name = "Tim"
    surname = "Smirnov"
    user = {"initials": name + " " + surname}
    return render_template('email-is-true.html', user=user)


@mn.route('/project', methods=('GET', 'POST'))  # чистим сессию и переходим на страницу без регистрации
def project():
    name = "Tim"
    surname = "Smirnov"
    user = {"initials": name + " " + surname}

    if request.method == 'POST':
        email = request.form['email']
        about = request.form['about']
        error = None

        if not email:
            error = "Email is required."
        elif not about:
            error = "Say something about you."

        if not validate_email(email, verify=True):  # проверка имейла на валидность (существование или корректность)
            error = "Your email is not valid :("

        if error is None:
            return render_template('we-will-write-you-soon.html', user=user)

        flash(error)

    return render_template('projects.html', user=user)
