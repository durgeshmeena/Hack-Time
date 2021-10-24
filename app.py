from typing import Tuple
from flask import Flask, request
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
import json
from decouple import config
import asyncio

from bs4 import BeautifulSoup
import regex as re 
import numpy as np
import pandas as pd 

from update_mlh_data import mlh_update
from update_cp_data import cp_update
from update_hackerearth_data import hackerearth_update
app = Flask(__name__)
app.secret_key = config('APP_SECRET')

session = {'Login':False, 'State':0, 'Loaded':False}

@app.route('/')
def index():
    return "Server Started"

def write(data):
    session['Loaded'] = True
    with open("data.json", "w") as database:
        json.dump(data, database) 

def go():
    data = '' # get_user(config('USER'), config('PASSWORD'))
    return  write(data)     


@app.route( '/bot', methods=['POST']) 
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    # handling session 

    if session['Login']:
        if 'mlh' in incoming_msg:
            mlh_update()
            msg.body('data updated')
            responded = True   

        if 'cp' in incoming_msg:
            cp_update()
            msg.body('data updated')
            responded = True     

        if '?' in incoming_msg:
            if session['Loaded']:
                msg.body('your data sucessfully loaded. \nReply with following to get imformation\n*1.* *General*- general information \n*2* *User*- user info \n*3.* *Balance*- balance Inquiry \n*4.* *Logout*- to end your session.')
                responded = True  
            else:
                msg.body('still Loading!. Please wait for few seconds')
                responded = True 

        if not session['Loaded']: 

            if 'start' in incoming_msg:
                go()
                msg.body("*Loading data*\nthis may take some time. Please reply with *?* to know status of your information")
                responded = True
    

            elif 'logout' in incoming_msg:
                session['Login'] = False
                session['Loaded'] = False
                with open("data.json", "w") as database:
                    json.dump({}, database) 
                msg.body('session ended sucessfully! \n*Thank you*')
                responded = True
            else:
                msg.body('your session alredy started. \n type *?* to know more.')     
                responded = True
                
   
        if session['Loaded']:
            if 'general' in incoming_msg:
                val = ""
                with open("data.json", "r") as database:
                    json_object = json.load(database)
                    val = json_object["1"]
                msg_str1 = '*Name:* '+val['Name']+'\n'+'*'+val['Account Status']+'*'+'\n'+'*VC_NO.*- '+val['VC_NO.']+'\n'+'*Model*- '+val['Model']+'\n'
                    
                msg.body(msg_str1)
                responded = True

            elif 'balance' in incoming_msg:
                val = ""
                with open("data.json", "r") as database:
                    json_object = json.load(database)
                    val = json_object["2"]

                msg_str2 = '*Acount balance till now:-* '+val['Balance_Today'] +'\n'+'*Last Recharge Amount*- ' +val['Last Recharge Amount']+'\n'+ '*Last Recharge Date*- '+val['Last Recharge Date']+'\n'+'*Next Recharge Date*- '+val['Next Recharge Date']+'\n' +'*Full Month Recharge*- '+ val['Full Month Recharge'] + '\n'
                  
                msg.body(msg_str2)
                responded = True

            elif 'user' in incoming_msg:
                val = ""
                with open("data.json", "r") as database:
                    json_object = json.load(database)
                    val = json_object["3"]

                msg_str3 = "*Name*- "+ val['Name'] + '\n' + '*Registered Telephone Number*- '+ val['Registered Telephone Number'] + '\n' + '*Registered Email ID*- ' + val['Registered Email ID'] + '\n' + '*Address*- ' + val['Address'] + '\n'

                msg.body(msg_str3)
                responded = True

            elif 'logout' in incoming_msg:
                session['Login'] = False
                session['Loaded'] = False
                with open("data.json", "w") as database:
                    json.dump({}, database) 
                msg.body('session ended sucessfully! \n*Thank you*')
                responded = True


            else:
                msg.body('Type *?* to know your command \n Type *START* to get your details or to send refresh command')     
                responded = True
            if not responded:
                msg.body('an Error occured! again Type *START* to start bot')  
         
    
    else:
        if "yes" in incoming_msg:
            session['Login'] = True
            msg.body("your session began \ntype *START*- To getting your information") 
            responded = True
        else:
            msg.body('*your session is not initialised* \nif you want to start your session reply with *YES*')
            responded = True             

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
