# class MainPage(webapp.RequestHandler):
#     def render_template(self, filename, context={}):
#         path = os.path.join(os.path.dirname(__file__), filename)
#         self.response.out.write(template.render(path, context))
#
#     def get(self):
#         self.render_template('index.html')
#
#
# application = webapp.WSGIApplication([('.*', MainPage), ], debug=False)

from flask import Flask, request, redirect, url_for, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for("gadget"))


@app.route('/level6/frame')
def gadget():
    return render_template("level6_index.html")


if __name__ == '__main__':
    app.run(debug=False)
