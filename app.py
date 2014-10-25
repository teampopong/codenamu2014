
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests
import ast
from collections import defaultdict
from operator import attrgetter
import json

app = Flask(__name__)

@app.route("/")
def hello():
	f = open('19th members.json', 'r')
	data = json.load(f)
	return render_template('person.html',data=data[0])

if __name__ == "__main__":
	app.run(debug=True)
