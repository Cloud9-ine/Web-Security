from flask import Flask, request, render_template, jsonify, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for("welcome"))


@app.route('/level5/frame/welcome')
def welcome():
    return render_template("level5_welcome.html")


@app.route('/level5/frame/signup')
def signup():
    return render_template("level5_signup.html", next=request.args.get("next"))


@app.route('/level5/frame/confirm')
def confirm():
    return render_template("level5_confirm.html", next=request.args.get("next", "welcome"))


if __name__ == '__main__':
    app.run(debug=False)
