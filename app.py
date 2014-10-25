
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests
import ast
from collections import defaultdict
from operator import attrgetter
import json

app = Flask(__name__)

from home import get_names

@app.route("/")
def home():
    return render_template('home.html', id_names=get_names()[:10])

@app.route("/<member_num>")
def hello(member_num):
	f = open('19th members.json', 'r')
	datas = json.load(f)
	data = datas[int(member_num)]
	data['yea'] = len([vote for vote in data['votes'] if vote['option'] == 'yea'])
	data['nay'] = len([vote for vote in data['votes'] if vote['option'] == 'nay'])
	data['forfeit'] = len([vote for vote in data['votes'] if vote['option'] == 'forfeit'])
	data['attend'] = len([attend for attend in data['attendance'] if attend])
	data['absent'] = len([attend for attend in data['attendance'] if not attend])
	return render_template('person.html',data=data)

if __name__ == "__main__":
	app.run(debug=True)
