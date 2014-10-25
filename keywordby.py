
# -*- coding: utf-8 -*-

from flask import Flask
import requests
import ast
from collections import defaultdict
from operator import attrgetter

app = Flask(__name__)

bill = [{'id':1, 'name':'회계연도  결산'},{'id':2, 'name':'회계연도  예비비지출 승인의 건'},{'id':3, 'name':'회계연도  결산 관련 감사원에 대한  감사요구안'}]
keywords = {'회계':[1,2,3]}

@app.route("/")
def hello():
	# 가장 참조 많이된 키워드? 혹은 편집된 키워드? 혹은 분리가 잘되는 키워드?
	# 1. 키워드별 의안 리스트 얻어오기
	# get keyword and bill

	# 2. 의안별 찬성/반대 데이터
	datas = requests.get("http://popong.com/~lucypark/tmp/19-329-5-%EB%B3%B8%ED%9A%8C%EC%9D%98.json").content
	datas = ast.literal_eval(datas)

	# index를 넣어줌
	for idx, data in enumerate(datas):
		data['id']=idx+1

	# 데이터 연결
	for keyword in keywords.keys(): 
		keywords[keyword] = [[datas[idx] for idx, data in enumerate(datas) if data['id'] == bill_id][0] for bill_id in keywords[keyword]]


	# 3. 찬/반이 달라진 의안 데이터에 경향 데이터 넣어주기
	for keyword in keywords.keys():
		keyword_bills = keywords[keyword]
		positive_groups = set(keyword_bills[0]['votes']['yea'])
		negative_groups = set(keyword_bills[0]['votes']['nay'])
		keyword_bills[0]['a_or_b'] = 'a' 
		for idx, bill in enumerate(keyword_bills):
			if idx > 0:
				if len(positive_groups.intersection(set(bill['votes']['nay'])))/len(positive_groups) > 0.7 and len(negative_groups.intersection(set(bill['votes']['yea'])))/len(negative_groups) > 0.7:
					bill['a_or_b'] = 'b'
				else:
					bill['a_or_b'] = 'a'

	# 4. 좀 더 많은 의안을 일단 찬성으로 하기(이건 좀 더 의안을 분석해야 기계적으로 인식 가능할 듯..) => 보류

	# 5. group by 키워드 (의원별 -> 찬&긍+반&부 : 반&긍+찬&부)
	groups = []
	for keyword in keywords.keys():
		keyword_bills = keywords[keyword]
		group_results = defaultdict(int)
		for bill in keyword_bills:
			val = 1 if bill['a_or_b'] == 'a' else -1
			for name in bill['votes']['yea']:
				group_results[name] = group_results[name] + val
			for name in bill['votes']['nay']:
				group_results[name] = group_results[name] - val
		group_results = [{"name":key,"data":group_results[key]} for key in group_results.keys()]
		groups.append({"keyword":keyword, "names":sorted(group_results, key=lambda result: 1000000-result['data'])})

	return str(groups)

if __name__ == "__main__":
	app.run()
