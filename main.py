from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.users import Jobs
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class RegisterForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/', methods=['GET', 'POST'])
def reqister():
    db_session.global_init("db/blogs.sqlite")
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            address=form.address.data,
            speciality=form.speciality.data,
            position=form.position.data,
            age=int(form.age.data)
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('reg.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
