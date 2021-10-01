from os import SEEK_CUR, name
from flask import Flask,request, jsonify, session
import json
import redis
import requests
import time
import ast

from requests.api import get

app = Flask(__name__)
r= redis.Redis(host='localhost',port=6379,)

@app.route("/hi")
def home():
    return "Hello, Flask!"


def check(uid):
    if r.get(uid)==None:
        sec=time.time()
        value={"count":5,"time":int(sec)}
        data= json.dumps(value)
        r.set(uid,data)
        return {'status': True, 'msg':"5 hit remaining in one minute"}
     
    else:
        current=int(time.time())
        val=r.get(uid)
        data=ast.literal_eval(val.decode('utf-8'))
        count=data['count']
        past=data['time']
        diff = abs(past-current)
        
        if diff<60:
            print("less than 60-",diff)
            if count>1:
                value={"count":count-1,"time":past}
                data= json.dumps(value)
                r.set(uid,data)
                val=count-1
                return {'status': True, 'msg': str(val)+" hit remaining in one minute"}
            else:
                return {'status': False, 'msg': "wait for "+str(60-diff)+" seconds"}
        else:
            value={"count":5,"time":current}
            data= json.dumps(value)
            r.set(uid,data)
            return {'status': True, 'msg': "5 hit remaining in one minute"}



@app.route('/stack',methods=['GET'])
def get_stack_overflow_data():
    uid=request.args.get("uid")
    response=check(uid)

    if response['status']==True:
        q=request.args.get('q')
        if r.get(q)==None:
            urls="https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&site=stackoverflow"
            Params={
                'q':q,
                'answers':int(request.args.get('answers')),
                'body':request.args.get('body'),
                'nottagged':request.args.get('nottagged'),
                'tagged':request.args.get('tagged'),
                'title':request.args.get('title'),
                'views':int(request.args.get('views'))
                }

            page= requests.get(urls,params=Params)
            d=page.json()
            data= json.dumps(page.text)
            r.set(q,data)
            return {"Message":response,"Data":d}
        else:
            d=r.get(q)
            data=d.decode("utf-8")
            data_json = json.loads(data)
            return {"Message":response,"Data":data_json}
    else:
        return response
