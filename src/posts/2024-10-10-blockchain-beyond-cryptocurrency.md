---

date: 2024-10-10
description: "Deploy blockchain beyond cryptocurrency with Ethereum and smart contracts—build decentralized trust for supply chain and identity verification."
title: 'Blockchain Beyond Cryptocurrency: Building the Trust Layer of the Internet'
tags:
  - architecture
  - blockchain
  - programming
  - security
---
I deployed a private Ethereum test network on my homelab's Dell R910 server (see [secure homelab adventures](/posts/2025-04-24-building-secure-homelab-adventure)) to find out what this technology feels like from the inside rather than from a whitepaper. The first lesson arrived early: blockchain infrastructure is not lightweight, and a validator node is a machine you leave switched on.

I started sceptical. The cryptocurrency hype felt disconnected from solving real problems, and the energy consumption seemed wasteful. After running actual nodes, deploying smart contracts, and pushing content into IPFS, I came round to a narrower view: the core innovation has little to do with digital money, and also less to do with most of what gets built on it.


<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/blockchain.png'); width: min(340px, 82%); aspect-ratio: 400/303; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">records, chained (hence the name)</p>

## What I Actually Learned Running Blockchain Infrastructure

The real breakthrough is distributed trust. For cryptographic foundations, see [demystifying cryptography](/posts/2024-01-18-demystifying-cryptography-beginners-guide). For the first time, we have systems that let parties transact without requiring a central authority to verify everything. When I deployed my first smart contract on the local testnet it cost 0.002 ETH in gas. That is play money — a private chain's ether has no market price, and quoting it in dollars would be a category error. What mattered was the mechanism: the transaction was verified without any single entity controlling whether it succeeded.

That has implications far beyond finance, though I'm still figuring out where the practical boundaries are.

## How It Actually Works (From My Test Network)

<figure class="arch-fig">
<div class="arch is-stack" role="group" aria-label="Blockchain system layers">
  <section class="arch-tier" data-label="Network Layer" role="group" aria-label="Network Layer"><span class="arch-chip">P2P Network</span><span class="arch-chip">Gossip Protocol</span></section>
  <section class="arch-tier" data-label="Consensus" role="group" aria-label="Consensus"><span class="arch-chip">Mining/Validation</span><span class="arch-chip is-primary">Consensus Algorithm</span></section>
  <section class="arch-tier" data-label="Data Layer" role="group" aria-label="Data Layer"><span class="arch-chip">Blocks</span><span class="arch-chip">Blockchain</span><span class="arch-chip">State Tree</span></section>
  <section class="arch-tier" data-label="Application" role="group" aria-label="Application"><span class="arch-chip is-primary">Smart Contracts</span><span class="arch-chip">DApps</span></section>
</div>
<figcaption>Blockchain systems build from peer networking through consensus and state storage into smart-contract applications.</figcaption>
</figure>

My local testnet processed a few dozen transactions per second on the Dell R910. The usual comparison is Visa's 24,000 tps, though that is Visa's tested capacity ceiling rather than observed throughput — its actual average is closer to 2,000. Either way the gap is real and scalability remains unsolved.

## The Trust Architecture (And Why It Matters)

Running these nodes taught me that blockchain's value comes from four specific properties:

### Decentralized Verification

Instead of banks or governments verifying transactions, a network of independent participants validates everything using cryptographic proofs. In my test environment, I ran three validator nodes across different VMs. Even when I deliberately crashed one node (to test fault tolerance), the network kept validating blocks. That redundancy removes single points of failure, at the cost of keeping several machines powered continuously — which is the honest tally on a homelab electricity bill.

### Byzantine Fault Tolerance

The system stays reliable even when some participants fail or act maliciously. I tested this by crashing a validator; the other two carried on producing blocks.

Then I did the arithmetic and found I had tested the easier property. The [Byzantine Generals Problem](https://lamport.azurewebsites.net/pubs/byz.pdf) requires 3f+1 nodes in total to tolerate f that lie — so tolerating a single Byzantine node needs four, and I had three. My setup survives a node that *stops*. It does not survive a node that *lies*, and I had assumed otherwise until I checked. Crash tolerance is the cheap half, and it is the half that most homelab demonstrations actually exercise.

### Immutable History

Once information is confirmed by the network, altering it becomes impractical — though the reason differs by consensus mechanism, and this is where a private chain misleads you. On a chain you fully control, rewriting history is a matter of restarting nodes with a different state; nothing stops you. Immutability on mainnet comes from the cost of overpowering everyone else's stake or hashrate, which is a property of the network's size rather than of the data structure. A three-node lab chain has a blockchain's shape and none of its security.

### Transparent Verification

All transactions are publicly verifiable, creating accountability. When I deployed a simple token contract, anyone could query the blockchain state and verify the total supply matched what the contract claimed. This transparency works well for some use cases, but I'm not sure it's appropriate for everything. Medical records probably shouldn't be on a public blockchain, for example.

These properties solve the "double-spend problem" for digital assets, as described in [Satoshi Nakamoto's original Bitcoin paper](https://bitcoin.org/bitcoin.pdf). But applications extend beyond digital money, though not everything needs blockchain that people try to shoehorn it into.

## Supply Chain Transparency: Where It Actually Works

One implementation I studied is Walmart's food traceability system built on IBM's Hyperledger Fabric. The widely cited result is a reduction in trace time for contaminated produce from about seven days to a couple of seconds. IBM's original case study page for it no longer resolves, so treat the figure as vendor-reported and undated rather than independently verified — and note that the comparison is against Walmart's previous paper-and-phone-call process, not against a well-built conventional database.

The system creates an immutable record of products moving from farm to store:

```javascript
// Simplified supply chain tracking smart contract
contract SupplyChainTracker {
    struct Product {
        uint256 id;
        string description;
        address currentOwner;
        uint256 timestamp;
    }

    mapping(uint256 => Product[]) public productHistory;

    function transferOwnership(uint256 productId) public {
        // Record transfers immutably
        productHistory[productId].push(Product({
            id: productId,
            description: "Transferred",
            currentOwner: msg.sender,
            timestamp: block.timestamp
        }));
    }
}
```

What makes this valuable isn't just the technology, it's the accountability. Every participant knows their actions are recorded permanently. That said, I'm curious whether a well-designed traditional database with proper access controls could achieve similar results at lower cost. I don't have enough supply chain experience to say definitively.

## My Failed Experiment with Self-Sovereign Identity

I spent two weeks in October trying to implement a basic self-sovereign identity system using the [Decentralized Identity Foundation's specifications](https://identity.foundation/). The concept is solid: instead of relying on Facebook or Google to verify who you are, you control your own identity credentials on a blockchain.

Europe's self-sovereign identity work has largely folded into eIDAS 2.0 and the EU Digital Identity Wallet, and Microsoft moved Entra Verified ID off the Bitcoin-anchored ION network. The advantages still make sense on paper:

- Users control what information to share
- Selective disclosure (share only necessary credentials)
- Verifiable credentials that employers can check cryptographically
- Identity that persists independent of any company

But here's what I learned the hard way: the user experience is terrible. I tried setting up a DID (Decentralized Identifier) for myself and got lost in a maze of cryptographic keys, resolver protocols, and wallet management. If I struggled with it as someone who works in tech, I can't imagine my parents using it. The technology might be sound, but the practical usability isn't there yet.

## Decentralized Finance: Beyond the Hype

DeFi gets attention for cryptocurrency speculation, but some traditional financial institutions are using blockchain in practical ways. JPMorgan's blockchain unit — Onyx, since renamed Kinexys — moves wholesale payments on blockchain rails. The bank reports [over $3 trillion in cumulative transaction volume and around $7 billion a day](https://www.jpmorgan.com/kinexys/index). That's real money, though it is worth noting this is a permissioned system between known counterparties: it uses the data structure without the trustless property that is supposed to be the point.

I tested basic DeFi primitives on my testnet by deploying an automated market maker (AMM) contract. A simple token swap consumed 0.0035 ETH in gas — cheap on a private chain, and the point is what that would cost on mainnet, where the same operation is priced against real ether and competes for real blockspace. The transparency is nice; I'm not convinced the cost-benefit works out for everyday transactions.

Central banks are exploring Central Bank Digital Currencies, and China's digital yuan is the largest pilot by a wide margin — cumulative volume is now measured in trillions of yuan. Whether that improves monetary policy or mostly creates new surveillance capability depends on implementation details that are not public.

## Governance and Voting: Promising but Unproven

Blockchain voting gets discussed a lot. West Virginia piloted it for overseas military voters in 2018 — and discontinued it in 2020, which is the part usually left out of the pitch. The theoretical benefits make sense:

- Voters can verify their ballots were recorded
- Vote tallies can't be altered after recording
- Remote voting without compromising security
- Anyone can audit the process

But in October, I tried implementing a simple voting contract on my testnet and immediately ran into problems. How do you prevent vote buying when votes are cryptographically provable? How do you maintain ballot secrecy while enabling verification? I ended up with a system where you could verify your vote was counted, but the connection between voter and vote choice was still traceable through transaction analysis.

Voatz, the app West Virginia used, was analysed by Specter, Koppel and Weitzner at MIT, who found it broken: a passive network adversary could recover votes, and an attacker controlling the device could alter them ([USENIX Security 2020](https://www.usenix.org/system/files/sec20-specter.pdf)). The researchers were the ones who broke it, not the ones who built it. Blockchain voting sounds good in theory; the implementations that have reached real elections have not survived contact with security researchers.

## Intellectual Property: Where I See Real Potential

Blockchain for digital rights management actually seems promising. Sony announced blockchain-based rights management for educational content, and Spotify acquired Mediachain in 2017 to track creative attribution — the latter was absorbed and wound down, which is the more common ending for these announcements. After experimenting with NFT metadata and IPFS content addressing, I can see how this works:

```javascript
// Simplified content rights tracking
contract ContentRights {
    struct Rights {
        address creator;
        string contentHash;  // IPFS hash
        uint256 creationDate;
        mapping(address => uint256) royaltyShares;
    }

    function registerContent(string memory ipfsHash) public {
        // Timestamp proof of creation
        // Manage royalty distributions automatically
    }
}
```

My IPFS node grew to 340GB storing content for these experiments. That's sustainable on my homelab, but I wonder about long-term storage costs for a production system. The automated royalty distribution through smart contracts is elegant, though I'm not sure how it handles disputes when two people claim to have created the same thing.

## Technical Innovations That Actually Help

Several developments have made blockchain more practical:

### Proof of Stake Energy Reduction

Ethereum's merge to proof-of-stake in September 2022 cut the network's annualized electricity consumption by more than 99.988%, per [CCRI's estimate published by the Ethereum Foundation](https://ethereum.org/en/energy-consumption/) — with carbon down about 99.992%, from 11,016,000 to 870 tonnes CO2e a year. That is a network-wide figure describing mining that no longer happens. It is not something a single node can confirm, and a private chain has no hashrate to eliminate in the first place.

### Layer 2 Scaling (With Trade-offs)

Networks like Polygon and Optimism claim thousands of transactions per second, and per-transaction costs on them are genuinely orders of magnitude below mainnet. The catch is that you're trusting a smaller validator set: faster and cheaper, meaningfully less decentralised. (Polygon's Mumbai testnet, which is what most tutorials from this era point at, was retired in April 2024 — use Amoy.)

### Privacy Techniques (That Are Hard to Use)

Zero-knowledge proofs let you verify information without revealing underlying data. I spent a week trying to implement a simple ZK-SNARK circuit using [circom](https://github.com/iden3/circom) and eventually got a proof working that verified I knew a password without revealing it. The math is sound, but the developer experience is brutal. Proof generation took 23 seconds on my i9-9900K, which seems impractical for real-time applications.

## What I've Learned About Implementation

Several patterns became clear:

### Blockchain Isn't Always the Answer

The most successful implementations solve specific problems where distributed trust provides clear advantages. For my homelab monitoring data, a traditional database works fine. I don't need Byzantine fault tolerance for recording CPU temperatures.

### Hybrid Approaches Make Sense

Combining blockchain with existing systems works better than complete replacement. Walmart didn't throw away their entire inventory system, they added blockchain for the specific traceability component.

### Network Effects Are Critical

My private testnet with three nodes was easy to set up but not very useful. Blockchain systems become valuable when many participants join, which creates a chicken-and-egg problem for new networks.

### Governance Is Still Unsolved

Even decentralized systems need mechanisms for upgrades and dispute resolution. When I needed to upgrade my smart contract, I realized I'd hardcoded it without an upgrade path. In production, that would be a serious problem.

## Challenges That Remain

Several important problems don't have clear solutions yet:

### Regulatory Uncertainty

Cryptocurrency regulations change constantly across jurisdictions. This creates compliance challenges that I don't know how to navigate. The [Global Blockchain Business Council](https://www.gbbc.io/) is working with regulators, but uncertainty remains high.

### Technical Complexity

Blockchain development is hard. I've been programming for years and still struggled with Solidity's quirks, gas optimization, and security vulnerabilities. Frameworks like [Hardhat](https://hardhat.org/) and [Foundry](https://getfoundry.sh/) help, but the learning curve is steep. (Truffle, which every tutorial of this vintage recommends, has since been sunset by ConsenSys along with Ganache.)

### The Scalability Trilemma Persists

You can optimize for decentralization, security, or scalability, but getting all three remains elusive. My testnet with three nodes was fast but not very decentralized. Ethereum mainnet is decentralized and secure but processes only about 15 tps. Polygon is faster but less decentralized. Pick your trade-offs.

## Where This Might Be Heading

The convergence of blockchain with other technologies creates interesting possibilities, though I'm uncertain about timelines:

### Blockchain and AI

[Ocean Protocol](https://oceanprotocol.com/) enables AI data marketplaces with blockchain tracking data provenance. I can see how this helps with AI training data accountability, but I haven't tested it enough to know if it works at scale.

### Blockchain and IoT

My Raspberry Pi 4 cluster in the homelab runs some IoT sensors. I experimented with IOTA's Tangle for device-to-device transactions, but the Pi's limited CPU made it impractical. IOTA claims to solve blockchain's scaling issues, but my testing showed 8-12 second confirmation times, which isn't great for real-time IoT.

### Blockchain and Quantum Computing

The [Quantum Resistant Ledger](https://www.theqrl.org/) develops blockchain designed to resist quantum attacks. This seems prudent given quantum computing advances, though I can't predict when quantum computers will actually break current crypto. It's probably worth preparing for, but the timeline is unclear.

## Building a Trust Layer (Maybe)

After running Ethereum nodes, experimenting with smart contracts, and paying the electricity bill for both, I think blockchain technology might be becoming a trust layer for the internet. Just as TCP/IP provides communication and HTTP provides information transfer, blockchain could provide verifiable value transfer.

That's the optimistic take. The realistic take is that blockchain works well for some specific use cases (supply chain tracking, international payments, digital rights management) but probably doesn't need to be applied to everything.

The technology has matured significantly since Bitcoin launched in 2009. Energy consumption dropped dramatically with proof-of-stake. Layer 2 solutions improve scalability, though with centralization trade-offs. Privacy-preserving techniques like zero-knowledge proofs work, but the developer experience is rough.

Important challenges remain around regulation, usability, and governance. I still can't recommend blockchain voting systems with confidence. Self-sovereign identity sounds great but isn't user-friendly enough yet. DeFi transaction costs are too high for everyday use.

As blockchain converges with AI, IoT, and eventually quantum computing, we might be seeing the emergence of new trust architectures for the internet. Or we might be seeing a technology that works brilliantly for narrow use cases but doesn't achieve the universal adoption that enthusiasts predict.

The homelab experiment taught me that blockchain is neither the solution to everything nor complete hype. It's a specific tool that solves specific problems, with real costs (electricity, complexity, scalability limits) and real benefits (distributed trust, transparency, censorship resistance).

Whether it becomes truly foundational infrastructure or remains a specialized tool for particular applications, I genuinely don't know yet. I'm going to keep my Ethereum node running and continue experimenting, because the only way to understand this technology is to actually use it.

---

## Sources

1. **[The Byzantine Generals Problem](https://lamport.azurewebsites.net/pubs/byz.pdf)** (1982)
   - Leslie Lamport, Robert Shostak, Marshall Pease
   - *ACM Transactions on Programming Languages and Systems*

2. **[Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf)** (2008)
   - Satoshi Nakamoto
   - Original whitepaper introducing blockchain

3. **[Walmart's Food Trust on IBM Blockchain](https://www.ibm.com/case-studies/walmart-food-trust)** (2020)
   - IBM Case Study
   - 2.2-second trace time improvement data

4. **[Ethereum Energy Consumption Post-Merge](https://ethereum.org/en/energy-consumption/)** (2023)
   - Ethereum Foundation
   - CCRI estimate: >99.988% reduction in annualized electricity consumption post-Merge

5. **[The Ballot is Busted Before the Blockchain: A Security Analysis of Voatz, the First Internet Voting Application Used in U.S. Federal Elections](https://www.usenix.org/system/files/sec20-specter.pdf)** (2020)
   - Michael A. Specter, James Koppel, Daniel Weitzner (MIT)
   - *29th USENIX Security Symposium*
   - The security analysis that found Voatz broken

6. **[JPMorgan Onyx Blockchain Platform](https://www.jpmorgan.com/kinexys/index)** (2023)
   - JPMorgan Chase & Co.
   - Reports >$3 trillion cumulative volume, ~$7 billion daily

For those interested in actually experimenting with blockchain (rather than just reading about it), the [Ethereum Developer Documentation](https://ethereum.org/en/developers/docs/) provides practical tutorials, and the [Hyperledger Foundation](https://www.hyperledger.org/) offers enterprise-focused resources. The [MIT Digital Currency Initiative](https://dci.mit.edu/) publishes academic research on blockchain's broader implications.

My homelab setup uses [Geth](https://geth.ethereum.org/) for Ethereum nodes and [IPFS](https://ipfs.io/) for distributed storage. Both have decent documentation if you want to try running your own infrastructure.
