# 💗The open source verifier

Dedicated for those who love [Algorand](https://www.algorand.foundation/impact-sustainability). For those who love crypto. The open source verifier is a bridge between off-chain code and on-chain apps. It is more than an API. Looking bigger, it is community-way to punish scams, and build trust for legitimate apps. In [one click](http://veri.algotool.app/), it verifies, if the on-chain app matches its Github source code. Results are stored forever in the Algorand blockchain itself.

In this way, we incentivize smart-contract open sourcing, explore projects and people worthy to trust.

## An outstanding technology

Out-of-the-box support for [Reach](https://developer.algorand.org/docs/get-started/dapps/reach/), [PyTeal](https://developer.algorand.org/docs/get-started/dapps/pyteal/), [Teal](https://developer.algorand.org/docs/get-details/dapps/avm/teal/). Instantlty spin, and scale as you need with Docker. See all commits of any file with advanced [Git support](https://github.com/ishepard/pydriller). It's like an alley of stars in Hollywood, but
for the best dApp Git repos.

This is not just a fancy figure of speech. Like those Hollywood stars are forever ingrained in stone. For each verified dApp, we spend a bit of ALGO, and send a transaction with a special message. This message looks like this:

```javascript
{
    message: {
        verified: "success",
        appId: 552635992,
        git: "https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_approval.teal",
        commit: "dc9ab40c58b85c15d58f63a1507e18be76720dbb",
    }
}
```

As a dApp user:

> Avoid scam. Navigate safely through the vast dApp sea. Sleep soundly.

As a dApp owner:

> Get audit and invesments easier. Become a thought leader within the community. Explore trusted source code to get inspiration. Be in the ever-upward flow of open source.

## A quick usage

Five minutes. Two steps. Easier than eating an 🍧.

However,
**Docker Compose** _MUST_ be installed. Here are [Instructions](https://docs.docker.com/compose/install/). On a _Windows_ machine, **Docker Desktop** comes with the necessary tools. Please see an excellent instruction for [Windows](https://github.com/algorand/sandbox#windows).

If you already have docker compose, then just change into to cloned repository dir.

```bash
git clone https://github.com/avalias/theopensourceverifier.git
cd theopensourceverifier
docker compose up
```

After those commands, the verifier must be up and running. To see the Web App, visit [http://127.0.0.1:1337](http://127.0.0.1:1337). It should look like our [hosted version](http://veri.algotool.app/). If you would like to see the FastAPI docs for the backend, visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## The community mission

Crypocurrency has always been intended to be [open, transparent, and honest](https://www.algorand.com/resources/blog/opensourceavailable/). Open source software shares the same spirit - be open, transparent, and honest. If a smart-contract owner hides the source code, it's a red flag. If the off-chain source code does not match, it's a big red flag.

In an ideal world, people would trust new financial opportunites. They would trust the smart-contract you wrote.
In reality, more and more crypto-savy people demand audit. Audit is expensive.

> The cost of smart contract audit services varies among providers and, generally, ranges between $5K and $30K for small and medium-sized projects. For large projects, the cost of a smart contract audit may reach $500K or even more.

We believe that creating a trustable app does not have to be expensive. Trasparent, open, and community-driven, as blockhain has always been intended. Surely, the open source verifier is not audit replacement. And, it was never meant.

Meet a new concept: community-audit.

## The community-audit

🌈Imagine, you have a github. You opened up to community. You open-sourced the Algorand smart-contract.
Industry leaders like it. They add stars. People dive deep into your Github. They write in discussion that your source is safe. Your app is worthy. The code is elegant.

In a certain way, the community has audited you.

Now, your github has huge trust. Yet, you still have a huge problem. There are two different worlds: on-chain and off-chain.
How do you prove that the bytecode you loaded on-chain is the same
one Would you like to loose trust?

The missing link is the open source verifier. Being a bridge between the two worlds. It proves . That's a solid proof that the upon reputable Github code is The proof is going to saved and insribed forever onto the blockchain.

$$ \text{Public github } + \text{Community audit} + \text{The open source verifier}= \text{Proven trust} $$

With the [open source verifier](http://veri.algotool.app/), you can trust the community and each other. Make the world of crypto a safer 💗🍧🍥🌸🐇🩰🏩💌🎀 place. Please, try the open source verifier [http://veri.algotool.app/](http://veri.algotool.app/)

## The tech details for 🦄nerds like us

The devil is in the details. So, here is a list of nerdy points:

- A small tip. If you have your own [Algorand Indexer](https://github.com/algorand/sandbox) running, just replace the address `algoexplorerapi.io` and `purestake.io` in `/api/verify.py` and `/web/app.py` with your local node, indexer addresses. They are compatible and interchangeable. Now, your verifier is completely independent of any side API.

- Just by changing a single line, you can incentivize authors to open-source best smart-contracts. As we store all succesfull verifications on the blockchain itself. We do a transaction. Change the recepient to the owner of the dApp. Set the reward ammount to something worthy. To filter out cheaters, just filter based on Github stars, forks, first commit date. Simple. Let the magic of open-source spread!

- [Streamlit](https://streamlit.io/) is used for the frontend. So, this project is indeed purely Pythonic. Anyone coming from Data Science and Physics like us, knows it's perfect for rapid prototyping. It's powerful. 
We separated API from the Web app. The `/api` folder has its own docker-compose.yaml file. So, after all prototyping-decisions made and finalized. React, Svelte, SolidJs, or any other framework in the world can be used for the Web. 

- Some people use Http requests, Github API, or good-old scraping to get the source code. Beware! The web version and API [have limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting). We use honest `git clone` command under the hood. Currently, in contrast to API, it's unlimited. Sleep soundly, while gazillions of Github repos can be verified.

- Yes! Out of the box, it supports the mighty three:
[Reach](https://developer.algorand.org/docs/get-started/dapps/reach/), [PyTeal](https://developer.algorand.org/docs/get-started/dapps/pyteal/), [Teal](https://developer.algorand.org/docs/get-details/dapps/avm/teal/). Even better, we managed to put all the three in one docker container. Unlike, other solutions, which can use Reach only outside of Docker. We natively support it. 
