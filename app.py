
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
	datas = json.load(f)
	data = datas[0]
	data['yea'] = len([vote for vote in data['votes'] if vote['option'] == 'yea'])
	data['nay'] = len([vote for vote in data['votes'] if vote['option'] == 'nay'])
	data['forfeit'] = len([vote for vote in data['votes'] if vote['option'] == 'forfeit'])
	data['attend'] = len([attend for attend in data['attendance'] if attend])
	data['absent'] = len([attend for attend in data['attendance'] if not attend])
	return render_template('person.html',data=data)

if __name__ == "__main__":
	app.run(debug=True)
