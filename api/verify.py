# To run reach from non-root
# sudo - u USERNAME

import glob
import json
import os
import requests
from subprocess import Popen, PIPE, run, call
from datetime import datetime


#TODO our own decompile method goal clerk -D better than on algoexplorer
#Do our own compile via goal clerk
#And maybe, if it is not slow and does not require whole running indexer node
#Do our own byteCode retrieval method

def compile(tealCode):
    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res = requests.post('https://node.algoexplorerapi.io/v2/teal/compile',
                        data=tealCode,
                        headers=newHeaders).json()

    if "result" in res.keys():
        return res["result"]

def byteCode(appId):
    res = requests.get(
        'https://indexer.algoexplorerapi.io/v2/applications/' + str(appId) + '?include-all=true')
    if (res.status_code == 200):
        appData = json.loads(res.text)
        approvalProgram = appData["application"]["params"]["approval-program"]
        return approvalProgram

def _makeTemp():
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    command = ["mktemp", "-d", "-t", 'tmp.{}.XXXXXX'.format(timestamp)]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    #p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    #output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    #rc = p.returncode
    return result.returncode, result.stdout, result.stderr

def makeTemp():
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    command = ["mktemp", "-d", "-t", 'tmp.{}.XXXXXX'.format(timestamp)]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result.stdout[:-1]

def reachToTeal(code):  
    tmpFolder = makeTemp()
    indexPath = os.path.join(tmpFolder, "index.rsh")
    with open(indexPath, 'w') as file:
        file.write(code)
    call(["reachc", indexPath, "--intermediate-files"])
    
    tealPath = os.path.join(tmpFolder, "build/index.main.appApproval.teal")
    teal = False
    try:
        with open(tealPath, 'r') as file:
            teal = file.read()          
    except:
        pass
    call(["rm", "-rf", tmpFolder])
    return teal

def pyTealToTeal(code):
    tmpFolder = makeTemp()
    indexPath = os.path.join(tmpFolder, "index.py")
    with open(indexPath, 'w') as file:
        file.write(code)
    call(["python", indexPath], cwd=tmpFolder)
    
    teal = False
    try:
        files = glob.glob(tmpFolder + "/*.teal")
        tealPath0 = files[0]
        tealPath = tealPath0
        if (len(files) > 1): 
            #Just for testing purpose we assume that bigger file is approval contract
            tealPath1 = files[1]
            tealSize1 = os.stat(tealPath1).st_size
            tealSize0 = os.stat(tealPath0).st_size
            if (tealSize1 > tealSize0): tealPath = tealPath1
     
        with open(tealPath, 'r') as file:
            teal = file.read()          
    except:
        pass
    call(["rm", "-rf", tmpFolder])
    return teal

#genreate http response

#teal = pyTealToTeal(pyTealCode)
#print(teal)

# compiledTeal = reachToTeal(reachCode)
# if compiledTeal:
#     print("ok")
#     print(compiledTeal)
# else:
#     print("failed")


#print(makeTemp())
#reachToTeal()
#print(byteCode(553829581))
#print(compile(tealCode))

