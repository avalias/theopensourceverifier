from examples import getPyTealExample, getTealExample, getReachExample
from mygit import lookUpRepo, lookUpRepoUrl, urlToRepoAndFilename
from verify import pyTealToTeal, reachToTeal, compile, byteCode, executePy
from typing import Union
from fastapi import FastAPI, Body, Response, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

class VerificationData(BaseModel):
    url_to_entry_file: str
    commit_hash: Union[str, None] = None
    app_id: int
    testnet: bool = False

@app.post("/build/py_repo")
def build_repo(git_file_url: str ):
#   ourcode = 
    #if compile_any(ourcode) == byteCode(appId):
    #res = compile_any("""
    teal = executePy()
    print(teal)
    return teal