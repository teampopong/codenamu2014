#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import json

def get_names():
    with open('members.json', 'r') as f:
        data = json.load(f)
    return [(i, d.get('name')) for i, d in enumerate(data)]
