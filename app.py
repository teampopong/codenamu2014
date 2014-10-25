# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests
import ast
from collections import defaultdict
from operator import attrgetter
import json

app = Flask(__name__)

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

@app.route("/<member_num>")
def member(member_num):
	f = open('members.json', 'r')
	datas = json.load(f)
	data = datas[int(member_num)]
	data['yea'] = len([vote for vote in data['votes'] if vote['option'] == 'yea'])
	data['nay'] = len([vote for vote in data['votes'] if vote['option'] == 'nay'])
	data['forfeit'] = len([vote for vote in data['votes'] if vote['option'] == 'forfeit'])
	data['attend'] = len([attend for attend in data['attendance'] if attend])
	data['attend_grade'] = calc_attend_grade(data)
	data['absent'] = len([attend for attend in data['attendance'] if not attend])
	return render_template('person.html',data=data)

if __name__ == "__main__":
	app.run(debug=True)
