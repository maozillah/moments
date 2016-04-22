from flask import Flask, render_template, jsonify, Response, request
from flask.ext.cors import CORS, cross_origin
import json
from instagram_scraper import igLocSearch
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/moment", methods=['GET', 'POST'])
@cross_origin()
def get_moment():
	if request.method == 'POST':
		clickPos = request.get_data()
		# print("posted to server " + clickPos)

		return jsonify(igLocSearch(clickPos))

@app.route("/")
@cross_origin()
def index():
    return render_template("index.html")

# def main():
#     data()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # main()
