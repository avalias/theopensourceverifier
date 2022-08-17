from dis import Bytecode
import pandas as pd
import streamlit as st
import json
import requests
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants
from array import *
import numpy as np
import time


def compileAny(anyCode):
    newHeaders = {'Content-type': 'text/plain', 'Accept': 'text/plain'}
    res = requests.post('http://api:8000/compile/any',
                        data=anyCode,
                        headers=newHeaders)
    return res.text


def byteCode(appId):  # function will get bytecode from app id from algoexplorer
    res = requests.get(
        'https://indexer.algoexplorerapi.io/v2/applications/' + str(appId) + '?include-all=true')
    if (res.status_code == 200):
        appData = json.loads(res.text)
        approvalProgram = appData["application"]["params"]["approval-program"]
        return approvalProgram


def gitresult(giturl):  # function will return teal code from selected commit
    newHeaders = {'Content-type': 'text/plain', 'Accept': 'application/json'}
    res = requests.post('http://api:8000/git/history',
                        data=giturl,
                        headers=newHeaders)
    commits = json.loads(res.text)
    st.write("We found", str(len(commits)), "commits.")
    st.write("Commit with hash:", commits[-1]['commit_hash'], "is the last.")

    commhashes = []
    for com in commits:
        commhashes.append(com['commit_hash'])

    option = st.selectbox(
        'What commit would you need to verify?',
        (commhashes), index=(len(commhashes)-1))

    neededcomm = next(
        x for x in commits if x['commit_hash'] == "{}".format(option))
    neededcommsource = neededcomm['source']
    neededcommcode = ("""{}""".format(neededcommsource))
    return neededcommcode


st.set_page_config(page_title="💗The open source verifier", page_icon=None)
st.title('💗The Open Source Verifier')

url = st.text_input("Enter git file url(pyteal/teal/reach) to compile:",
                    value="https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_approval.teal")
if len(url) != 0:
    ourcode = gitresult(url)

appId = st.text_input("App Id On-Chain:", value="552635992")

if len(appId) != 0:
    if byteCode(appId) == None:
        #st.write("Bad AppId")
        st.markdown('<p style="font-family:Source Sans Pro, sans-serif;; font-style: normal;font-weight: 400; color:Red; font-size: 18px;">Bad App Id</p>', unsafe_allow_html=True)

if "my_list" not in st.session_state:
    st.session_state.my_list = []

form = st.form(key="annotation")
with form:
    submitted = st.form_submit_button(label="Verify")
    if submitted:
        if len(url) != 0 and len(appId) != 0 and compileAny(ourcode) != None and byteCode(appId) != None:
            if compileAny(ourcode) == byteCode(appId):
                st.header("Result: Equal")
                st.markdown(
                    "Each verified contract makes the world of crypto a safer 💗🍧🍥🌸🐇🩰🏩💌🎀 place. We appreciate your impact.")
            else:
                st.header("Result: not Equal")
        else:
            st.write("Bad inputs")
