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
    if request.args.get("next") == "confirm":
        return render_template("level5_signup.html", next=request.args.get("next"))
    else:
        return render_template("level5_signup.html")


@app.route('/level5/frame/confirm')
def confirm():
    if request.args.get("next", "welcome") == "welcome":
        return render_template("level5_confirm.html", next=request.args.get("next", "welcome"))
    else:
        return render_template("level5_confirm.html")


if __name__ == '__main__':
    app.run(debug=False)
