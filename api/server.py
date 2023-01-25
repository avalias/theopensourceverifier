from examples import getPyTealExample, getTealExample, getReachExample
from mygit import lookUpRepo, lookUpRepoUrl, urlToRepoAndFilename
from verify import executePy, pyTealToTeal, reachToTeal, compile, byteCode
from transacting import checker, send_transaction
from typing import Union
from fastapi import FastAPI, Body, Response, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel


class VerificationData(BaseModel):
    build_argument: str = "contracts.escrow.contract"
    url_to_build_file: str = "https://github.com/thaddavis/kalygo_contracts/blob/main/build.sh"
    commit_hash: Union[str, None] = ""
    app_id: int = 155880853
    testnet: bool = True


class Arc23VerificationData(BaseModel):
    app_id: int
    testnet: bool = False


class Code(BaseModel):
    code: str


    # class Config:
    #     schema_extra = {
    #         "example": "Your pyteal code goes here"
    #     }
description = """For all those who love Algorand. The open source verifier API is a bridge between off-chain code and on-chain apps. Automaticaly verify Algorand smart-contracts.
Avoid scams. If their github source code does not match the actual on-chain app, you will know it.  

Out-of-the-box support for Reach, PyTeal, Teal. See all commits of any file with advanced Git support.

Trust the community and each other. Make the world of crypto a safer 💗🍧🍥🌸🐇🩰🏩💌🎀 place. Try some of the examples below.

Try the first route /match/pyteal_app, if you want to intgegrate our verification for your app.

"""
app = FastAPI(title="💗The open source verifier",
              description=description, version=7.1)


pyTealExample = getPyTealExample()
tealExample = getTealExample()
reachExample = getReachExample()

# (domain, company, repo, filePath, fileName) = urlToRepoAndFilename("https://github.com/algorand/smart-contracts/blob/master/devrel/crowdfunding/crowd_fund.teal")
# commits, sources = lookUpRepo((domain, company, repo, filePath, fileName))
# print(commits, sources)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


@app.post("/match/pyteal_app")
def match_app(data: VerificationData):
    git_file_url = data.url_to_build_file
    ourcode, commhash = build_repo(git_file_url, data.build_argument)
    # Store git hash somewhere
    print("Ourcode", ourcode)
    compiled_code = compile_teal(ourcode)
    byte_code = byteCode(data.app_id,  testnet=data.testnet)
    if data.testnet:
        net = "testnet"
    else:
        net = "mainnet"
    # print("Compiled_code", compiled_code)
    # print("Byte_code", byte_code)
    print("Commit hash", commhash)
    if compile_teal(ourcode) == byte_code:
        checked, link = checker(data.app_id)
        if checked == False:
            algoexplorer_link = send_transaction(
                net, data.app_id, data.url_to_build_file, data.build_argument, str(commhash))
        else:
            algoexplorer_link = link
        return {"status": "verified", "proof_link": algoexplorer_link}
        # check not posted verification transaction
        # if not post
        # add current commit hash calculated
        # add if testnet
        # add entry file
        # build_command
        # copy from app py use new .env key
        pass
    # Get
        # res = compile_any("""
    print(data.url_to_build_file)
    # print(res)
    return "Non verified"


@app.post("/git/history")
def git_history(gitUrl: str = Body(..., example="https://github.com/algorand/smart-contracts/blob/master/devrel/crowdfunding/crowd_fund.teal", media_type="text/plain")):
    # print("Im reading")
    return lookUpRepoUrl(gitUrl)

# TODO return which error exactly if it was not compiled


@app.post("/build/py_repo")
def build_repo(git_file_url: str, build_argument: str = ""):
    teal, commhash = executePy(git_file_url, build_argument=build_argument)
    print(teal)
    return teal, commhash


@app.post("/compile/any", response_class=PlainTextResponse)
def compile_any(code: str = Body(..., example=pyTealExample, media_type="text/plain")):
    code1 = code.strip()
    determiner = code1[0:7]
    print(determiner)
    if (determiner == """#pragma"""):
        teal = code
    elif (determiner == "'reach "):
        teal = reachToTeal(code)
    else:
        teal = pyTealToTeal(code)
    result = compile(teal)
    return result


@app.post("/compile/pyteal", response_class=PlainTextResponse)
def compile_pyteal(code: str = Body(..., example=pyTealExample, media_type="text/plain")):
    print(code)
    result = compile(pyTealToTeal(code))
    return result


@app.post("/compile/teal", response_class=PlainTextResponse)
def compile_teal(code: str = Body(..., example=tealExample, media_type="text/plain")):
    result = compile(code)
    return result


@app.post("/compile/reach", response_class=PlainTextResponse)
def compile_reach(code: str = Body(..., example=reachExample, media_type="text/plain")):
    result = compile(reachToTeal(code))
    return result


@app.post("/tealify/reach", response_class=PlainTextResponse)
def tealify_reach(code: str = Body(..., example=reachExample, media_type="text/plain")):
    result = reachToTeal(code)
    return result


@app.post("/tealify/pyteal", response_class=PlainTextResponse)
def tealify_pyteal(code: str = Body(..., example=pyTealExample, media_type="text/plain")):
    result = pyTealToTeal(code)
    print("result:", result)
    return result
# code: Code

# pragma version for some reason pyteal gives wrong pragma version too old like 2. I had to fix it by hand manually
# Is it wrong to patch it to 6 everywhere. Is it backward compatible
# patch name if it changes it can be not _approval for the case
# if __name__ == "__main__":
#     with open("vote_approval.teal", "w") as f:
#         compiled = compileTeal(approval_program(), mode=Mode.Application)
#         f.write(compiled)

#     with open("vote_clear_state.teal", "w") as f:
#         compiled = compileTeal(clear_state_program(), mode=Mode.Application)
#         f.write(compiled)
# Here is a bad example https://github.com/algorand/pyteal/blob/master/examples/application/opup.py

# class Item(BaseModel):
#     name: str
#     description: Union[str, None] = None
#     price: float
#     tax: Union[float, None] = None

#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Foo",
#                 "description": "A very nice Item",
#                 "price": 35.4,
#                 "tax": 3.2,
#             }
#         }

# TODO: to make it pretty - create tags and descriptions
# https://fastapi.tiangolo.com/tutorial/metadata/
# Attach good schemas to Body everywhere
# https://fastapi.tiangolo.com/tutorial/schema-extra-example/
