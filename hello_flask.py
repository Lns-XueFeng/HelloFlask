import click
from flask import Flask
from flask import url_for, render_template


app = Flask(__name__)
# 配置的方式, 还可以使用文件进行配置
app.config["HelloConfig"] = "Yes I'm"
app.config.update(
    TESTCONFIG=True,
    SECRET_KEY="_5#fjasfnlawfnagkj",
)


@app.route("/")
def index():
    return "<h1>Hello Flask</h1>"


@app.route("/hi")
@app.route("/hello/<name>")
def hello(name="Programmer"):
    return "<h1>Hello {}</h1>".format(name.title())


@app.route("/URL_FOR_example")
def url_for_example():
    return "<h1>Here is URL_FOR: {}</h1>" \
        .format(url_for(endpoint="url_for_example"))


@app.cli.command()
def show_hi_in_shell():
    click.echo("Hi Lns-XueFeng")


@app.route("/hello_template")
def hello_template():
    return render_template("hello.html")


if __name__ == "__main__":
    app.run()   # 不推荐的flask运行方法
