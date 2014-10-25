# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests
import ast
from collections import defaultdict
import json

app = Flask(__name__)

datas = None
with open('members.json') as f:
	datas = json.load(f)

candidacies = None
with open('candidacies.json') as f:
    candidacies = json.load(f)
districts = defaultdict(list)
for candidacy in candidacies:
    candidacy['district'] = candidacy['district'][1:-1].replace(',', ' ')
    district_ids = candidacy['district_ids'][1:-1].split(',')
    if district_ids[0].isdigit():
        districts[int(district_ids[0])].append(candidacy)

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
    return render_template('home.html')

@app.route("/map")
def map():
    return render_template('map.html')

@app.route("/<member_id>")
def member(member_id):
    data = datas[member_id]
    data['laws'] = json.dumps(data['sponsored_laws'])
    data['yea'] = len([v for v in data['votes'] if v['option'] == 'yea'])
    data['nay'] = len([v for v in data['votes'] if v['option'] == 'nay'])
    data['forfeit'] = len([v for v in data['votes'] if v['option'] == 'forfeit'])
    data['attend'] = len([a for a in data['attendance'] if a['attendance']])
    data['attend_grade'] = calc_attend_grade(data)
    return render_template('person.html',data=data)

@app.route("/map/<int:region_id>")
def region(region_id):
    candidates = districts[region_id]
    return render_template('region.html', candidates=candidates, datas=datas)

if __name__ == "__main__":
    app.run(debug=False)

