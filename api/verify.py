# To run reach from non-root
# sudo - u USERNAME

import glob
import json
import os
import shutil
import subprocess
import tempfile
from urllib.parse import urlparse
import requests
from subprocess import Popen, PIPE, run, call
from datetime import datetime


# TODO our own decompile method goal clerk -D better than on algoexplorer
# Do our own compile via goal clerk
# And maybe, if it is not slow and does not require whole running indexer node
# Do our own byteCode retrieval method

def compile(tealCode):
    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res = requests.post('https://node.algoexplorerapi.io/v2/teal/compile',
                        data=tealCode,
                        headers=newHeaders).json()

    if "result" in res.keys():
        return res["result"]


def byteCode(appId, testnet=False):
    indexer = 'https://indexer.algoexplorerapi.io/v2/applications/'
    if testnet:
        indexer = 'https://indexer.testnet.algoexplorerapi.io/v2/applications/'
    res = requests.get(
        indexer + str(appId) + '?include-all=true')
    if (res.status_code == 200):
        appData = json.loads(res.text)
        approvalProgram = appData["application"]["params"]["approval-program"]
        return approvalProgram


def _makeTemp():
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    command = ["mktemp", "-d", "-t", 'tmp.{}.XXXXXX'.format(timestamp)]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    # p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    # output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    # rc = p.returncode
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
        files = glob.glob(tmpFolder + "/**.teal", recursive=True)
        tealPath0 = files[0]
        tealPath = tealPath0
        if (len(files) > 1):
            # Just for testing purpose we assume that bigger file is approval contract
            tealPath1 = files[1]
            tealSize1 = os.stat(tealPath1).st_size
            tealSize0 = os.stat(tealPath0).st_size
            if (tealSize1 > tealSize0):
                tealPath = tealPath1

        with open(tealPath, 'r') as file:
            teal = file.read()
    except:
        pass
    call(["rm", "-rf", tmpFolder])
    return teal


def findOutTeal(files):
    teal = False
    print(files)
    try:
        tealPath0 = files[0]
        tealPath = tealPath0
        if (len(files) > 1):
            # Just for testing purpose we assume that bigger file is approval contract
            tealPath1 = files[1]
            tealSize1 = os.stat(tealPath1).st_size
            tealSize0 = os.stat(tealPath0).st_size
            if (tealSize1 > tealSize0):
                tealPath = tealPath1

        with open(tealPath, 'r') as file:
            teal = file.read()
    except:
        pass
    return teal


def pyTealToTeal(code):
    tmpFolder = makeTemp()
    indexPath = os.path.join(tmpFolder, "index.py")
    with open(indexPath, 'w') as file:
        file.write(code)
    call(["python", indexPath], cwd=tmpFolder)
    files = glob.glob(tmpFolder + "/**.teal", recursive=True)
    teal = findOutTeal(files)
    call(["rm", "-rf", tmpFolder])
    return teal


def executePy(url, build_argument=""):
    # Extract github repository and file path
    parsed_url = urlparse(url)
    github_repo = parsed_url.path.split(
        '/')[1] + '/' + parsed_url.path.split('/')[2]
    github_file = '/'.join(parsed_url.path.split('/')[5:])

    # Clone a github repository to a temporary directory
    temp_dir = tempfile.mkdtemp()
    subprocess.run(
        ['git', 'clone', 'https://github.com/' + github_repo, temp_dir], )

    commhash = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=temp_dir)
    # Snapshot all existing .teal files
    teal_files_before = set(glob.glob(temp_dir + '/**/*.teal', recursive=True))

    # Execture the file with python in shell
    if github_file.endswith('.py'):
        subprocess.run(['python3', github_file, build_argument], cwd=temp_dir)

    if github_file.endswith('.sh'):
        subprocess.run(['sh', github_file, build_argument], cwd=temp_dir)
    # Find all new .teal files that appeared in temp folder after execution
    teal_files_after = set(glob.glob(temp_dir + '/**/*.teal', recursive=True))
    new_teal_files = teal_files_after - teal_files_before
    print(teal_files_after)
    teal = findOutTeal(list(new_teal_files))
    print(teal)
    # Remove the temporary directory
    shutil.rmtree(temp_dir)

    return teal, commhash

# genreate http response

# teal = pyTealToTeal(pyTealCode)
# print(teal)

# compiledTeal = reachToTeal(reachCode)
# if compiledTeal:
#     print("ok")
#     print(compiledTeal)
# else:
#     print("failed")


# print(makeTemp())
# reachToTeal()
# print(byteCode(553829581))
# print(compile(tealCode))
