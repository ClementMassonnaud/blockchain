---
title: "My understanding of the bitcoin protocol"
---


# What are the issues with digital money?

The main issue with digital money is that it is very easy to copy or tamper data over internet connections. It is traditionally dealt with by relying on a central authority, which is there to guarantee transactions and settle disputes. 

Bitcoin is a system of digital money with two main caracteristics:

1. it does not depend on any central authority. The system is entirely distributed
2. it does not require trust

These two points are distinct, and equally important. Relying on a central authority necessarily imply trust toward that authority. However, the fact that a system that is completely distributed does not imply that it is trustless.

## A distributed system

The solution to avoid having to rely on a central authority, is to give every node on the network a copy of the entire history of all transactions (distributed ledger). When a new transaction is made, it is broadcasted over the entire network, so that every participant can verify its validity, and record the transaction on its copy of the ledger.

This looks simple enough, but it raises serious problems. Nodes on a computer network cannot be simply trusted, even less than a central authority. We need a system that is secure as long as the majority of nodes is honest.

## A trustless system

For a truly distributed digital money system to work, it must be 100% trustless. Each participant must not have to trust other participants, but instead must require *proof* on key aspects.

### Identity

Since every participant has a full copy of all transactions, it would be easy to find a participant that has a substantial amount of money, and fake a transaction.

Let's say I am Bob, and I see on the ledger that Alice has 1 bitcoin. What prevents me to broadcast to the entire network: "Alice sends 1 bitcoin to Bob."?

This problem is resolved via the use of cryptography and digital signatures. Each participant has one or more unique digital signatures, which he will use to sign transaction messages. Cryptography protocols guarantee that each signature is unique, and that it is impossible to copy or falsify a signature. Therefore, it is impossible for Bob to create a message on Alice's behalf since he cannot sign the message with Alice's signature (as long as she keeps her signature secret and secured).


### Validity of information

Now that we are confident that identities cannot be forged, we still need to be sure that transactions are valid. If Bob hears the message that Alice sends him 1 bitcoin, he will verify that Alice has not already spent this 1 bitcoin by looking through the history of transactions on his own copy of the ledger.

However, how can Bob be sure that his personal copy of the ledger is correct? That is, how can he be sure that the majority of the network has the same history of transactions as the one he is looking at?

Even if he could ask every participant in the network if they do have the same version of the ledger, he doesn't want to have to *trust* their answer, he wants *proof* that the majority of the network has indeed the same version of the ledger.

This problem of *consensus* over a computer network is the main issue with digital money, and it is the key solution that was introduced by bitcoin.

### Immutability of information

Even after having found a way to guarantee identities, and a way to ensure that the majority of nodes agree on the same version of the ledger, we still need to make sure that it is not possible to alter the history of transactions. That is, the ledger should be append-only, and it should not be possible to change previously written transactions.

If Bob has sent his last bitcoin to Alice, he will not be able to send another bitcoin to Charlie after that, because Charlie will be aware of the transaction to Alice, since everyone is sharing the same version of the ledger, thanks to the consensus mechanism. But if Bob finds a way to make the majority of the network agree to "erase" the transaction to Alice *after* it has been made, he would be able to spend his bitcoin a second time (say to Charlie) since the transaction to Alice no longer exists. This is known as the *double spend* problem, a key problem with digital money, at it is that key problem that bitcoin managed to address.

The problem is more subtle than it might look at first glance. After all, why would the majority of the network agree to change previous transactions, since they already agreed on them? And even if Bob controls more than 50% of the network, why would Charlie himself agree to the transaction with Bob, since Charlie has seen the previous transaction to Alice, and has seen that it was reverted. After all, Bob cannot erase the transaction from the memory of Charlie.


## The double-spend problem

Let's look carefully at how this would work.

1. Bob sends 1 bitcoin to Alice
2. Alice confirms that the transaction is valid, and makes sure that the majority of nodes has also acknowledged this transaction (through the consensus mechanism)
3. Alice sends something back to Bob to complete the exchange (say the equivalent amount in dollars, or a car)
4. Once Bob is sure Alice is no longer able to take back what she sent him, he will try to make the majority of nodes switch to another version of the shared ledger. That is, he will propose a version of the history of transactions that no longer shows the transaction to Alice, and make the majority of the network agree on this alternative version through the consensus mechanism.
5. Once the majority of the network has switched to Bob's version of the ledger, he can now send his bitcoin again, this time to Charlie, thus spending it a second time.

The bitcoin system found a way to make such an attempt basically impossible if Bob controls less that 50% of the network, but even not necessarily profitable even if he controls more than 50% of the network (known as 51% attack).

Howevever, this whole process raises a number of important questions, that are often not addressed when presenting bitcoin. Thanks to the consensus mechanism, it is impossible for Bob to send one version of the ledger to Alice, and another version to Charlie at the same time, because both Alice and Charlie can make sure that their version is shared by the majority of nodes. It means that, when Bob broadcasted the transaction to Alice, Charlie *must* have been aware of it. In that case, why is Charlie willing to accept the second transaction later on, since he his necessarily aware that the version of the ledger has changed, and that the bitcoin he his receiving was registered as sent to Alice?

In other words, why the protocol should allow nodes to change their version of the ledger to modify previously registered transactions?




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


