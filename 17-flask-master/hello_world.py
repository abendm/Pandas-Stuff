import flask
app = flask.Flask(__name__)

@app.route("/")
def hello():
	return "<h1>Hello World!</h1>"

@app.route("/greet/<name>")
def greet(name):
	return "Hello, {}!".format(name)

if __name__ == '__main__':
	app.run(debug=True)