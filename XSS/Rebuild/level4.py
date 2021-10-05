from flask import Flask, redirect, url_for, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for("level"))


@app.route('/level4/frame')
def level():
    if request.method == 'GET':
        if not request.args.get('timer'):
            return render_template('level4_index.html')
        else:
            timer = request.args.get('timer')
            return render_template("level4_timer.html", timer=timer)


if __name__ == '__main__':
    app.run(debug=False)
