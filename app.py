import os
from flask import Flask, request, session, render_template, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd 
from decouple import config
from update_mlh_data import mlh_update
from update_cp_data import cp_update
from update_hackerearth_data import hackerearth_update
app = Flask(__name__)
app.secret_key = config('APP_SECRET')

@app.route('/')
def index():
    return render_template("base.html") 

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route( '/bot', methods=['POST']) 
def bot():
    # print(session['login'])
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()
    # session = {'login':False, 'loaded':True, 'catagory':None, 'stage':0, 'CP':{ 'catagory':False, 'stage':0 }, 'MLH':{ 'catagory':False, 'stage':0 }, 'Hack':{ 'catagory':False, 'stage':0 }, }
    if "show" in incoming_msg:
        session['login'] = True
        session['loaded'] = True
        session['catagory'] = None
        session['cp'] = 0
        session['mlh'] = 0
        session['hack'] = 0
        response.message('Choose one of the following to get imformation\n*1.* *Hackathon*- for Hackathons \n*2* *CP*- Contest \n[ _after_ _loading_ _eventdata_, \n_type_ *_Next_* _to_ _load_ _more_ _data_ ] \n\n*?*- for other commands')
        return str(response)
    else:
        if 'login' in session:
            pass
        else:
            response.message('*Welcome user* \nwe are one step solution for all hackathons and contest \ntype *Show* to show available options')
            return str(response)               
        

    if session['login']:
        if '?' in incoming_msg:
            if session['loaded']:
                response.message('\n*1.* *Hackathon*- for Hackathons \n*2.* *CP*- Contest \n *3.* *Home*- for home \n *4.* *Logout*- for ending session \n *5.* *UpdateM*- for refreshing MLH events data \n *6.* *UpdateC*- for refreshing Contest events data \n *7.* *UpdateO*- for refreshing Other Hackathons events data \n *8.* *Next*- to load more next data')
                responded = True  
            else:
                response.message('still Loading!. Please wait for few seconds')
                responded = True 

        if not session['loaded']: 

            if 'mlh' or 'cp' or 'hacks' or 'updatemlh' or 'updatecp' or 'updatehacks' in incoming_msg:
                response.message("*Loading data*\nthis may take some time. Please reply with *?* to know status of your information")
                responded = True
    

            elif 'logout' in incoming_msg:
                session.clear()
                response.message('session ended sucessfully! \n*Thank you*')
                responded = True
            else:
                response.message('your session alredy started. \n type *?* to know more.')     
                responded = True
                
   
        if session['loaded']:
            if 'hackathon' in incoming_msg:
                response.message('Choose one of the following to get imformation\n*1.* *MLH*- for Mlh Hackathons \n*2.* *Other*- for Other Hackathons')
                responded = True

            elif 'other' in incoming_msg:
                session['catagory'] = 'hack'
                df = pd.read_csv('data_hackerearth.csv')
                i = 0
                session['hack'] = session['hack']+5
                # print('i=',i, ' --- ', 'new stage= ', session)
                while i<=session['hack']:
                    msg = response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Status: ' +'*'+df.iloc[i, :]['Status']   +'*'+'\n' + 'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n' + 'Company: ' + '*'+df.iloc[i, :]['Company']  + '*'+'\n'+ 'Registrations/Prize: ' + '*'+  str( df.iloc[i, :]['Registrations/Prize'] ) + '*'+'\n'  )
                    msg.media(df.iloc[i,:]['image'])
                    if i==session['hack']:
                        response.message('type *Next* to load more...')
                    i+=1
                responded = True     

            elif 'mlh' in incoming_msg:
                session['catagory'] = 'mlh'
                df = pd.read_csv('data_mlh.csv')
                i = session['mlh'] = 0
                session['mlh'] = session['mlh']+5
                # print('i=',i, ' --- ', 'new stage= ', session)
                while i<=session['mlh']:
                    msg = response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Date/Time: ' +'*'+df.iloc[i, :]['Date/Time']   +'*'+'\n' + 'Length: ' +'*'+df.iloc[i, :]['Length']     +'*'+'\n' +  'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Location: ' + '*'+df.iloc[i, :]['Location'] +'*'+'\n' +       'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n'  )
                    msg.media(df.iloc[i,:]['Image'])
                    if i==session['mlh']:
                        response.message('type *Next* to load more...')
                    i+=1
                responded = True                        
              

            elif 'cp' in incoming_msg:
                session['catagory'] = 'cp'
                df = pd.read_csv('data_cp.csv')
                i = session['cp'] = 0
                session['cp'] = session['cp']+5
                # print('i=',i, ' --- ', 'new stage= ', session)
                while i<=session['cp']:
                    response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Date/Time: ' +'*'+df.iloc[i, :]['Date/Time']   +'*'+'\n' + 'Length: ' +'*'+df.iloc[i, :]['Length']     +'*'+'\n' +  'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Location: ' + '*'+df.iloc[i, :]['Location'] +'*'+'\n' +       'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n'  )
                    if i==session['cp']:
                        response.message('type *Next* to load more...')
                    i+=1
                responded = True

            elif 'next' in incoming_msg:
                       
                if session['catagory'] == 'cp':
                    df = pd.read_csv('data_cp.csv')
                    i = session['cp']
                    session['cp'] = session['cp']+5
                    while i<session['cp']:
                        response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Date/Time: ' +'*'+df.iloc[i, :]['Date/Time']   +'*'+'\n' + 'Length: ' +'*'+df.iloc[i, :]['Length']     +'*'+'\n' +  'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Location: ' + '*'+df.iloc[i, :]['Location'] +'*'+'\n' +       'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n'  )
                        i+=1

                elif session['catagory'] == 'hack':
                    df = pd.read_csv('data_hackerearth.csv')
                    i = session['hack'] 
                    session['hack'] = session['hack']+5
                    while i<session['hack']:
                        msg = response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Status: ' +'*'+df.iloc[i, :]['Status']   +'*'+'\n' + 'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n' + 'Company: ' + '*'+df.iloc[i, :]['Company']  + '*'+'\n'+ 'Registrations/Prize: ' + '*'+  str( df.iloc[i, :]['Registrations/Prize'] ) + '*'+'\n'  )
                        msg.media(df.iloc[i,:]['image'])
                        i+=1

                elif session['catagory'] == 'mlh':
                    df = pd.read_csv('data_mlh.csv')
                    i = session['mlh']
                    session['mlh'] = session['mlh']+5
                    while i<session['mlh']:
                        msg = response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Date/Time: ' +'*'+df.iloc[i, :]['Date/Time']   +'*'+'\n' + 'Length: ' +'*'+df.iloc[i, :]['Length']     +'*'+'\n' +  'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Location: ' + '*'+df.iloc[i, :]['Location'] +'*'+'\n' +       'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n'  )
                        msg.media(df.iloc[i,:]['Image'])
                        i+=1
                response.message('type *Next* to load more...') 
                responded = True

            elif 'updatem' in incoming_msg:
                mlh_update()
                response.message('Updating Data!!')
                responded = True    

            elif 'updateo' in incoming_msg:
                hackerearth_update()
                response.message('Updating Data!!')
                responded = True    

            elif 'updatec' in incoming_msg:
                cp_update()
                response.message('Updating Data!!')
                responded = True                    

            elif 'home' in incoming_msg:
                response.message('Choose one of the following to get imformation\n*1.* *Hackathon*- for Hackathons \n*2* *CP*- Contest')
                responded = True

            elif 'logout' in incoming_msg:
                session.clear()
                response.message('session ended sucessfully! \n*Thank you*')
                responded = True


            else:
                response.message('Type *?* to know your command')     
                responded = True
            if not responded:
                response.message('an Error occured! again Type *START* to start bot')              

    return str(response)

