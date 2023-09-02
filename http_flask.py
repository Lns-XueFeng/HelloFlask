import os

from flask import Flask
from flask import request, make_response, redirect, url_for, abort, session, g, current_app


app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Http与Flask</h1>"


@app.route("/request")
def request_object():
    path = request.path
    url = request.url
    args = request.args
    cookies = request.cookies
    files = request.files
    form = request.form
    headers = request.headers
    method = request.method
    referer = request.referrer
    user_agent = request.user_agent
    data_dict = {
        "资源地址": path,
        "完整url": url,
        "查询字符串": args,
        "cookies": cookies,
        "上传文件": files,
        "表单数据": form,
        "请求头:": headers,
        "请求方法": method,
        "请求源": referer,
        "User_Agent": str(user_agent),
    }
    html_str = ""
    for k, v in data_dict.items():
        h2_label = f"<h2>{k}: {v}</h2>"
        html_str += h2_label
    return html_str


# 最安全的返回发是将密钥写入系统环境变量或者是.env文件中
app.secret_key = "secret string" or os.getenv("SECRET_KEY", "secret string")
# or SECRET_KET = "secret string"


@app.route("/login", methods=["GET", "POST"])
def login():
    account_data = request.form
    if account_data:
        # 当我们使用session对象添加cookie时, 数据会使用程序已经设置好的密钥对其进行签名
        # 加密后的数据存储在一块名为session的cookie中
        session["logged_in"] = True   # 写入session
    return "<h1>假装有一个登录界面</h1>"


@app.route("/passages/<int:count>")
def passages(count):
    count_list = [1, 2, 3, 4, 5]
    if count in count_list:
        pass
    return "<h1>假装有一个文章集锦</h1>"


@app.route("/mk_response")
def mk_response():
    response = make_response(
        "<h1>响应主体、状态码、首部字段</h1>",
        201,
        # {"Location", "https://www.example.com"},
    )
    response.mimetype = "text/plain"
    # or response.headers["Content-Type"] = "text/plain; charset='utf-8'"
    if not request.cookies:
        name = request.args.get("name", "Programmer")
        response.set_cookie(key="name", value=name)
    if request.cookies.get("name") == "Lns-XueFeng":
        print("管理员来啦！！！")
    return response


@app.route("/redirect")
def re_direct():
    return redirect(url_for("response"))


@app.route("/forbid")
def forbid():
    return abort(404)


@app.before_request
def do_something1():
    g.name = "程序上下文：存储全局变量(每次请求的！！！)"


# @app.after_request
# def do_somthing2():
#     pass


@app.route("/flask_context")
def flask_context():
    """
    current_app
    g
    request
    session
    """
    get_g_name = g.name   # 拿到存储在g对象中的本次请求的全局变量
    return f"<h1>{get_g_name}</h1>"


@app.route("/activate_context")
def activate():
    """
    flask run
    app.run()
    执行@app.cli.command()注册的flask命令时
    flask shell
    """
    with app.app_context():
        current_ap = current_app.name

    with app.test_request_context(url_for("index")):
        method = request.method
    """这两个上下文在Python Shell演示为佳"""
    return f"<h1>{current_ap} {method}</h1>"


if __name__ == "__main__":
    app.run()
