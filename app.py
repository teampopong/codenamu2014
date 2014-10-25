# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests
import ast
from collections import defaultdict
from operator import attrgetter
import json

app = Flask(__name__)

datas = None
with open('members.json', 'r') as f:
	datas = json.load(f)

from utils import get_names

def calc_attend_grade(data):
    rate = data['attend']/float(len(data['attendance']))
    if 0.95 < rate:
        return 'A+'
    elif 0.90 < rate:
        return 'A'
    elif 0.85 < rate:
        return 'B'
    elif 0.80 < rate:
        return 'C'
    elif 0.75 < rate:
        return 'D'
    elif 0.70 < rate:
        return 'F'


@app.route("/")
def home():
    return render_template('home.html', id_names=get_names())

@app.route("/map")
def map():
    return render_template('map.html')

@app.route("/<int:member_num>")
def member(member_num):
	data = datas[int(member_num)]
	data['yea'] = len([v for v in data['votes'] if v['option'] == 'yea'])
	data['nay'] = len([v for v in data['votes'] if v['option'] == 'nay'])
	data['forfeit'] = len([v for v in data['votes'] if v['option'] == 'forfeit'])
	data['attend'] = len([a for a in data['attendance'] if a['attendance']])
	data['attend_grade'] = calc_attend_grade(data)
	return render_template('person.html',data=data)

if __name__ == "__main__":
	app.run(debug=True)
