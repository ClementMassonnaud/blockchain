---
title: "My understanding of the bitcoin protocol"
---


# What are the issues with digital money?

- I could easily fake being someone else
- It's hard to make all participants agree on the same history of transactions without a central authority
  - if I have the majority of nodes, I can write whatever transactions I want
  - all nodes are not connected equally, so there is asymetry of information. Some nodes will hear some transactions, some will hear others.
  

# I could fake being someone else

This is "easily" solved by public key cryptography

# If I have the majority of nodes, I can write whatever transactions I want
## What's the issue?

You cannot really write any transaction.

We need to think about what a transaction is, and what it means to make a fraudulent transaction. If I am malicious, the way to make profit from a transaction is to convince someone to send me something *in exchange* of what I am sending her, but actually never sending her anything (or taking it back), while keeping what I received.

But for her to send me what I want in the first place, she needs to be convinced herself that the transaction is valid. Indeed, it doesn't matter if I make 99.9% of the network fake that the transaction is valid, if she cannot verify it herself, she will not accept the transaction. A digital money protocol must be 100% trustless, so you will never accept a transaction even by trusting 99.9% of the network. You must be able to verify every transaction by yourself.

So to make a fraudulent transaction, I would first need to send a valid transaction, say a coin to Alice, who will be able to confirm that it is valid. Then, I would need to wait to receive what I want in exchange, and secure it.

But then, to *actually* make profit from the fraudulent transaction, I not only have to take my coin back, I aslo need to spend that same coin at least a second time. If I'm not able to do so, I've just deprived Alice of her coin, but I haven't made a profit for myself, which would be pretty much worthless. So now, to spend my coin a second time, I need to convince someone else, say Bob, that the transaction to Alice actually never happened.

So, to make a profit, I need to be able to re-write the history of the transactions, so that Bob thinks I never sent the coin to Alice. If I own 99.9% of the nodes in the network, this is pretty easy to do. Even if I own only 51% of the network, it would be a dispute between the nodes that think Alice's transaction came first and the nodes that think it was Bob's. And the majority would win.

## How do we deal with it?

We deal with this issue by making it quite hard to rewrite the history of transactions. We do that in two ways: 

- it is computationally expensive to write a transaction. To write a transaction, we need to solve a puzzle by finding a random number, which is relatively hard to find. But once found, everyone in the network can verify that it is correct very easily. So if I want to convince Bob that the transaction with Alice never happened, I need to redo the computational work again, otherwise Bob will not consider the transaction valid. 
- each transaction added to the ledger, actually each block of transactions, is linked to the previous block in such a way that, if I want to rewrite a transaction in a block in the middle of the chain, I not only need to rewrite that block, but also all subsequent blocks, adding to the computational expense.

So, for a fraudulent transaction to be profitable, the reward must exceed the computational expense. Therefore, to be safe, Alice just has to wait a little bit to make sure that the computational work needed to rewrite her transaction makes it worthless to attempt it, even if the attacker controls a large proportion of the network.


