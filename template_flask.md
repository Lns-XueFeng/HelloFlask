## Template_Flask


### 模板语法
```jinja2
{{ ... }} 表达式：比如字符出、变量、函数调用等
{% ... %} 语句：比如if语句、for循环等
{# ... #} 注释
```

```jinja2
{% if user.bio %}
    <i>{{ user.bio }}</i>
{% else %}
    <i>This user has not provided a bio</i>
{% endif %}


{% if user.bio %}
    <i>{{ user.bio }}</i>
{% elif user.dio %}
    <i>{{ user.dio }}</i>
{% else %}
    <i>This user has not provided a bio or dio</i>
{% endif %}


{% for value in value_list %}
    {% if value % 2 == 1 %}
        <i>{{ value }} is odd</i>
    {% else %}
        <i>{{ value }} is pdd</i>
    {% endif %}
{% endfor %}
```

### 渲染模板
```python
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
```

### *上下文
模板上下文包含了很多变量，其中包括我们调用render_template函数时手动传入的变量以及Flask默认传入的变量，
除了渲染时传入变量，你也可以在模板中定义变量，使用set标签：
```jinja2
{% set navigation = [('/', 'Home'), ('/about', 'About')] %}

{# 也可以将一部分模板数据定义为变量 #}
{% set navagation %}
    <li><a href="/">Home</a>
    <li><a href="/about">About</a>
{% endset %}
```
```text
内置上下文变量：config、request、session、g
```
```python
# 自定义上下文

from flask import Flask

app = Flask(__name__)

@app.context_processor
def inject_foo():
    foo = 'I am foo'
    return dict(foo=foo)
'''
返回值必须为字典，
这些返回值会被添加到模板中，
因此我们可以在模板中直接使用foo变量
'''

# or app.context_processor(function)
```

### 全局对象
全局对象是指在所有的模板中都可以直接使用的对象
```text
内置全局函数：
Jinja2内置的：range(), lipsum(), dict()
Flask内置的：url_for(), get_flashed_message()
```
```python
# 自定义全局函数

from flask import Flask

app = Flask(__name__)

@app.template_global()
def bar():
    return "I am bar."
```

### 过滤器
在Jinja2中，过滤器是一些可以用来修改和过滤变量的特殊函数。
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
    <div>{{name | title}}</div>
</body>
</html>
```
```text
default, escape, first, last, length, random, safe, truncate
trim, max, min, unique, striptags, tojson, urlize, wordcount
```

```python
# 自定义过滤器
from flask import Flask
from flask import Markup

app = Flask(__name__)


@app.template_filter
def musical(s):
    return s + Markup(' &#9835')
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
    <div>{{name | musical}}</div>
</body>
</html>
```

### 测试器
在Jinja2中，测试器是一些用来测试变量或表达式，返回布尔值的特殊函数。
```jinja2
{% if age is number %}
    {{ age * 365 }}
{% else %}
    无效的数字
{% endif %}
```
```text
内置的常用测试器函数自行查阅
```

### 模板环境对象
在Jinja2中，渲染行为由jinja2.Environment类控制，所有的"配置选项"，"上下文变量"，"全局函数"，"过滤器"和"测试器都存储在该实例对象上。
当与Flask结合后，并不单独的创建Environment对象，而是使用Flask创建的Environment对象，它存储在app.jinja_env属性上。
知道这有什么用呢？
模板环境中的全局函数、过滤器、测试器分别存储在Environment对象的globals、filters、tests属性中，它们都是字典对象。
因此除了使用Flask提供的装饰器去注册自定义函数，其实也可以通过向对应的字典属性中添加键值对来实现，传入模板的名称为键，对应的函数对象为值。
```python
from flask import Flask

app = Flask(__name__)

def bar():
    return "I am bar."

foo = "I am foo"

app.jinja_env.globals["bar"] = bar
app.jinja_env.globals["foo"] = foo
```
```python
from flask import Flask

app = Flask(__name__)

def smiling(s):
    return s + " :)"

app.jinja_env.filters["smiling"] = smiling
```
```python
from flask import Flask

app = Flask(__name__)

def baz(n):
    if n == "baz":
        return True
    return False

app.jinja_env.tests["baz"] = baz
```
### 局部模板
如何插入一个局部模板？？？
利用include即可
```jinja2
{% include '_banner.html' %}
```

### 宏
类似于函数
```jinja2
{% macro qux(amount=1) %}
    {% if amount == 1 %}
        I am qux
    {% elif amount > 1 %}
        We are qunxs
    {% endif %}
{% endmacro %}
```
为了方便可以把宏存储在单独的文件中，需要时导入即可，此文件一般命名为macros.html
```jinja2
{% from "macros.html" import qux %}

{{ qux(amount=5) }}
```

### 模板继承
base.html
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{% block title %}我是基模板{% endblock %}</title>
</head>
<body>
    <nav>
        <ul><li><a href="{{url_for('index')}}">Home</a></li></ul>
    </nav>
    <main>
        {% block maincontent %}{% endblock %}
    </main>
    <footer>
        {% block endcontent %}{% endblock %}
    </footer>
    {% block script %}{% endblock %}
</body>
</html>
```
index.html
```html
{% extends "extends.html" %}
{% from "macros.html" import qux %}

{% block content %}
......
{% endblock %}
```

### 空白控制
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
    {% for i in li -%}
        <h1>{{i}}</h1>
    {%- endfor %}
</body>
</html>
```

### 加载静态文件
依靠url_for函数

### 消息闪现
flash 提示弹出
get_flashed_message 获取flash弹出的消息

### 自定义错误界面
```python
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.errorhandler(404)
def not_found():
    return render_template("personlize_error_page.html")
```

### JS及CSS中的Jinja2
可以将jinja2的语法写入但不推荐