tealCode = """#pragma version 2
// deploy app first then get id
// replace id in this teal to create
// the escrow address
// use goal app update to set the
// escrow address
global GroupSize
int 2
==
gtxn 0 TypeEnum
int 6
==
&&
gtxn 0 ApplicationID
int 1
==
&&
gtxn 0 OnCompletion
int NoOp
==
&&
"""

reachCode ="""'reach 0.1';
'use strict';

export const main = Reach.App(() => {
  const A = Participant('Alice', {
    request: UInt,
    info: Bytes(128),
  });
  const B = Participant('Bob', {
    want: Fun([UInt], Null),
    got: Fun([Bytes(128)], Null),
  });
  init();

  A.only(() => {
    const request = declassify(interact.request); });
  A.publish(request);
  commit();

  B.only(() => {
    interact.want(request); });
  B.pay(request);
  commit();

  A.only(() => {
    const info = declassify(interact.info); });
  A.publish(info);
  transfer(request).to(A);
  commit();

  B.only(() => {
    interact.got(info); });
  exit();
});
"""

pyTealCode = """
from pyteal import *

def app():
    handle_noop = Seq(
        Assert(Txn.application_args[0] == Bytes("payme")),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum : TxnType.Payment,
            TxnField.amount : Int(5000),
            TxnField.receiver : Txn.sender()
        }),
        InnerTxnBuilder.Submit(),
        Int(1)
    )

    return Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.NoOp, Return(handle_noop)]
    )

if __name__=='__main__':
    with open("escrow.teal", "w") as f:
        compiled = compileTeal(app(), mode=Mode.Application, version=5)
        f.write(compiled)
"""

def getTealExample():
    return tealCode

def getPyTealExample():
    return pyTealCode

def getReachExample():
    return reachCode