from dis import Bytecode
import pandas as pd
import streamlit as st
import json
import requests
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk import transaction
from algosdk import constants
from array import *
import numpy as np
import time
from transtest import send_transaction, checker
import re
st.title('The Open Source Verifier')



def compileAny(anyCode):
    newHeaders = {'Content-type': 'text/plain', 'Accept': 'text/plain'}
    res = requests.post('http://api:8000/compile/any',
                        data=anyCode,
                        headers=newHeaders)
    return res.text

def byteCode(appId): #function will get bytecode from app id from algoexplorer
    res = requests.get(
        'https://indexer.algoexplorerapi.io/v2/applications/' + str(appId) + '?include-all=true')
    if (res.status_code == 200):
        appData = json.loads(res.text)
        approvalProgram = appData["application"]["params"]["approval-program"]
        return approvalProgram
    
def gitresult(giturl):
    newHeaders = {'Content-type': 'text/plain', 'Accept': 'application/json'}
    res = requests.post('http://api:8000/git/history',
                        data=giturl,
                        headers=newHeaders)
    commits = json.loads(res.text)
    st.write("We found",str(len(commits)),"commits.")
    st.write("Commit with hash:",commits[-1]['commit_hash'],"is the last.")
    
    commhashes = []
    for com in commits:
        commhashes.append(com['commit_hash'])
    
    option = st.selectbox(
        'What commint do you need to verify?',
        (commhashes), index = (len(commhashes)-1))
    
    neededcomm = next(x for x in commits if x['commit_hash'] == "{}".format(option))
    neededcommsource = neededcomm['source']
    neededcommcode = ("""{}""".format(neededcommsource))
    neededcommHash = neededcomm['commit_hash']
    return neededcommcode, neededcommHash

url = st.text_input("Enter git file url(pyteal/teal/reach) to compile:", value = "https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_approval.teal")
if len(url) != 0:
    ourcode,neededcommHash = gitresult(url)

appId = st.text_input("App Id On-Chain:", value = "552635992")

if len(appId)!=0:
    if byteCode(appId) == None:
        st.markdown('<p style="text-align: center;font-family:Source Sans Pro, sans-serif;; font-style: normal;font-weight: 400; color:Red; font-size: 18px;">Bad App Id</p>', unsafe_allow_html=True)

if "my_list" not in st.session_state:
    st.session_state.my_list = []


form = st.form(key="annotation")
with form:
    color = "white"
    m = st.markdown("""<style>
    div.stButton > button:first-child {
        background-color: """+color+""";
        color: black;
        height: 3em;
        width: 12em;
        border-radius:10px;
        border:3px solid #000000;
        font-size:20px;
        font-weight: bold;
        margin: auto;
        display: block;
    }

    div.stButton > button:hover {
    background:linear-gradient(to bottom, """+color+""" 1%, #F9B0BF 100%);
    background-color:"""+color+""";
    }

    </style>""", unsafe_allow_html=True)
    submitted = st.form_submit_button(label="Verify")
    if submitted:
        if len(url)!=0 and len(appId)!=0 and compileAny(ourcode)!=None and byteCode(appId)!=None:
            if compileAny(ourcode) == byteCode(appId):
                st.markdown('<p style="text-align: center;font-family:Source Sans Pro, sans-serif;; font-style: normal;font-weight: 400; color:black; font-size: 18px;">✅Successfull verification!</p>', unsafe_allow_html=True)
                if checker(appId) == False:
                    send_transaction(appId, url, neededcommHash)
            else:
                st.markdown('<p style="text-align: center;font-family:Source Sans Pro, sans-serif;; font-style: normal;font-weight: 400; color:black; font-size: 18px;">❌Unsuccessfull verification!</p>', unsafe_allow_html=True)
        else:
            #st.write("Bad inputs")
            pass


data = requests.get("https://algoindexer.testnet.algoexplorerapi.io/v2/accounts/5W67A2ZEQYOQWIXN4PXV2T6QK3NNM25LQIWY7QNYFGODBWIF77TWAFHCOQ/transactions?limit=999").json()

history = []

txsNumber = len(data["transactions"])

i = 1
while i <= (txsNumber):
    try:
        if data['transactions'][i-1]['sender'] == "5W67A2ZEQYOQWIXN4PXV2T6QK3NNM25LQIWY7QNYFGODBWIF77TWAFHCOQ":
            id = data['transactions'][i-1]['id']
            note1 = data['transactions'][i-1]['note']
            history.append({
                'id':id,
                'note':json.loads(base64.b64decode(note1).decode())
            })
    except: pass
    i +=1

appIdHistory = []
giturlHistory = []
commitIdHistory = []
txidHistory = []

for transactionnumber in history:
    neededid =transactionnumber['note']['AppId']
    appIdHistory.append(f'<a target="_blank" href="https://algoexplorer.io/application/{neededid}">{neededid}</a>')

    giturl = transactionnumber['note']['GitUrl']
    giturlRegexp = "^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)\/([^:\/?\n]+)\/([^:\/?\n]+)"
    giturlHistory.append(f'<a target="_blank" href="{giturl}">{giturl[:70]+"..."}</a>')

    matches = re.search(giturlRegexp, giturl)
    domain = matches.group(1)
    company = matches.group(2)
    repo = matches.group(3)

    newlink = "https://"+domain+"/"+company+"/"+repo+"/commit/"+transactionnumber['note']['CommitHash']
    commhash = transactionnumber['note']['CommitHash']
    commitIdHistory.append(f'<a target="_blank" href="{newlink}">{commhash[:10]+"..."}</a>')

    txid = transactionnumber['id']
    txidHistory.append(f'<a target="_blank" href="https://testnet.algoexplorer.io/tx/{txid}">{txid[:10]+"..."}</a>')

df = pd.DataFrame({
    'App Id': appIdHistory,
    'Github url': giturlHistory,
    'Commit Id': commitIdHistory,
    'Transation Id': txidHistory
})

st.write(df.to_html(escape=False, index=False, justify="center"), unsafe_allow_html=True)

