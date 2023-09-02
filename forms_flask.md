## Forms_Flask


### 定义表单类
```python
from flask import Flask
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


app = Flask(__name__)
app.secret_key = "This is a secret_key"


class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired(), ])
    password = PasswordField("Passage", validators=[DataRequired(), Length(8, 14), ])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")


@app.route("/")
def login():
    lg = LoginForm()
    username = lg.username()
    password = lg.password()
    remember = lg.remember()
    submit = lg.submit()
    print(username, password, remember, submit)
    return lg.username.name + username + lg.password.name + password + remember + submit


if __name__ == "__main__":
    app.run()
```
在template中使用
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <form method="post">
        {{ lg.csrf_token }}<br>
        {{ lg.username.label }}:{{ lg.username(class="form_control") }}<br>
        {{ lg.password.label }}:{{ lg.password(class="form_control") }}<br>
        {{ lg.remember.label }}:{{ lg.remember(class="form_control") }}<br>
        {{ lg.submit(class="form_control")}}
    </form>
</body>
</html>
```
一个表单由若干个字段组成, 因此WTForms通过定义不同的字段类来实现不同的表单字段<br>
通过修改字段类中有参数label, render_kw, validators, default<br>
通过修改render_kw参数可以修改html标签的属性从而达到可以修改样式<br>
validators参数为将要设置的验证器去验证输入值是否符合特定情况<br>
此外还可以通过在调用字段时传入要设置的属性：lg.username(style="width: 200px", class_="bar")


### 验证表单数据
```python
from flask import Flask
from flask import url_for, render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


app = Flask(__name__)
app.secret_key = "This is a secret_key"


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), ])
    password = PasswordField("Passage", validators=[DataRequired(), Length(8, 14), ])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")


@app.route("/")
def login():
    lg = LoginForm()
    if lg.validate_on_submit():
        username = lg.username.data
        flash("{}，欢迎回来！！！".format(username))
        redirect(url_for('index'))
    return render_template("login.html", lg=lg)
```
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <form method="post">
        {{ lg.csrf_token }}<br>
        {{ lg.username.label }}:{{ lg.username(class="form_control") }}<br>
        {% for error in lg.username.errors %}
            <small>{{error}}</small>
        {{ lg.password.label }}:{{ lg.password(class="form_control") }}<br>
        {% for error in lg.password.errors %}
            <small>{{error}}</small>
        {{ lg.remember.label }}:{{ lg.remember(class="form_control") }}<br>
        {{ lg.submit(class="form_control")}}
    </form>
</body>
</html>
```

### 上传文件
文件其实也是表单的一种，类型变了一下，因此用字段FileField即可
```python
from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileSize, FileAllowed, FileRequired

app = Flask(__name__)


class FileForm(FlaskForm):
    file = FileField(
        "upload", 
        validators=[FileRequired(), FileAllowed(["jpg", "jpeg"], FileSize(3*1024*1024))]
    )

@app.route("/")
def upload():
    ff = FileForm()
    if ff.validate_on_submit():
        file_name = ff.file.name
        """......"""
    return render_template("upload.html", ff=ff)
```
