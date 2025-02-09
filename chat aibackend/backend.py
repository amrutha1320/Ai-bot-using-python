from flask import Flask,request,jsonify 
from pymongo import MongoClient
from openai import OpenAI

'''openaikey='xxxxxxx' '''
openai_mode='api'

# openai.api_key=openaikey
openaiclient=OpenAI(api_key=openaikey)
def generate_response(prompt):
    s=''
    response = openaiclient.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",stream=True)
    for chunk in response:
        if(chunk.choices[0].delta.content):
            s+=chunk.choices[0].delta.content
    return (s)

client=MongoClient('127.0.0.1',27017)
db=client['ChatAi'] 
collection=db['Chat_Ai'] 

api=Flask(__name__)

@api.route('/register',methods=['get']) 
def register():
     name=request.args.get('name')
     emailid=request.args.get('emailid')
     mobile=request.args.get('mobile')
     password=request.args.get('password')
     k={} 
     k['name']=name 
     k['emailid']=emailid
     k['mobile']=mobile
     k['password']=password 
     query={'emailid':emailid,'mobile':mobile}
     for i in collection.find(query):
         return ('account exist')
     collection.insert_one(k) 
     return('data stored') 

@api.route('/login',methods=['get'])
def     login():
    username=request.args.get('username')
    password=request.args.get('password')
    query={'mobile':username}
    for i in collection.find(query):
         if(i['password']==password):
            return 'True'
    return 'False'

@api.route('/chat', methods=['get'])
def chat():
    user_message = request.args.get('message')  
    bot_response = generate_response(user_message)
    response = {'message': bot_response}
    return jsonify(response)


if __name__=="__main__":
    api.run(host='0.0.0.0',port=2000,debug=True)