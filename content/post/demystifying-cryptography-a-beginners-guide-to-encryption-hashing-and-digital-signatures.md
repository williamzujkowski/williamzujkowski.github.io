+++
title = 'Demystifying Cryptography a Beginners Guide to Encryption Hashing and Digital Signatures'
date = 2024-04-08T00:00:39-04:00
draft = false
+++

# Demystifying Cryptography a Beginners Guide to Encryption Hashing and Digital Signature

In today's digital world, where sensitive information is constantly being
transmitted and stored online, cryptography plays a crucial role in
maintaining security and privacy. Cryptography, the art and science of secure
communication, provides the tools and techniques necessary to protect data
from unauthorized access and tampering. This post will provide a beginner-
friendly introduction to the fundamental concepts of cryptography, exploring
different types of encryption, hashing algorithms, and digital signatures.

### Encryption: Keeping Secrets Secret

Encryption is the process of transforming plaintext (readable data) into
ciphertext (unreadable data) using an algorithm and a secret key. Only
individuals possessing the correct key can decrypt the ciphertext back into
its original plaintext form. There are two primary types of encryption:

  * **Symmetric Encryption:**
    * **Definition:** Symmetric encryption uses the _same_ secret key for both encryption and decryption. Think of it like a shared secret code between two parties.
    * **How it works:** The sender encrypts the plaintext using the shared secret key and sends the ciphertext to the receiver. The receiver then uses the same secret key to decrypt the ciphertext and retrieve the original plaintext.
    * **Advantages:** Symmetric encryption is generally faster and more efficient than asymmetric encryption, making it suitable for encrypting large amounts of data.
    * **Disadvantages:** The key distribution problem is a major challenge. Securely sharing the secret key between parties can be difficult.
    * **Examples:**
      * [Advanced Encryption Standard (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
      * [Data Encryption Standard (DES)](https://en.wikipedia.org/wiki/Data_Encryption_Standard) \- (Note: DES is now considered outdated and insecure for most applications)
      * [Twofish](https://en.wikipedia.org/wiki/Twofish)
      * [Serpent](https://en.wikipedia.org/wiki/Serpent_\(cipher\))
  * **Asymmetric Encryption (Public-Key Cryptography):**
    * **Definition:** Asymmetric encryption uses _two_ different keys: a **public key** for encryption and a **private key** for decryption. The public key can be freely distributed, while the private key must be kept secret. 
    * **How it works:** The sender encrypts the plaintext using the receiver's public key. Only the receiver, who possesses the corresponding private key, can decrypt the ciphertext.
    * **Advantages:** Solves the key distribution problem of symmetric encryption. Public keys can be shared openly without compromising security. Enables digital signatures.
    * **Disadvantages:** Generally slower and less efficient than symmetric encryption.
    * **Examples:**
      * [RSA (Rivest-Shamir-Adleman)](https://en.wikipedia.org/wiki/RSA_\(cryptosystem\))
      * [Elliptic Curve Cryptography (ECC)](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography)
      * [Diffie-Hellman Key Exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)

### Hashing Algorithms: Ensuring Data Integrity

Hashing algorithms are one-way functions that take an input (of any size) and
produce a fixed-size output, called a hash or message digest. Hashes are used
to verify data integrity and are essential for digital signatures, password
storage, and other security applications.

  * **Key Properties of Hashing Algorithms:**
    * **Deterministic:** The same input will always produce the same hash output.
    * **One-way:** It is computationally infeasible to reverse the process and derive the original input from the hash.
    * **Collision-resistant:** It is extremely difficult to find two different inputs that produce the same hash output (a collision).
    * **Avalanche Effect:** A small change in the input should result in a significant change in the hash output.
  * **Common Hashing Algorithms:**
    * [SHA-2 (Secure Hash Algorithm 2)](https://en.wikipedia.org/wiki/SHA-2) \- A family of hash functions that includes SHA-256 and SHA-512. 
    * [SHA-3 (Secure Hash Algorithm 3)](https://en.wikipedia.org/wiki/SHA-3) \- The latest member of the Secure Hash Algorithm family.
    * [MD5 (Message Digest 5)](https://en.wikipedia.org/wiki/MD5) \- (Note: MD5 is now considered cryptographically broken and should not be used for security-critical applications due to collision vulnerabilities).
  * **Applications of Hashing:**
    * **Password Storage:** Instead of storing passwords in plaintext, websites often store a hash of the password. This way, even if the database is compromised, the actual passwords are not revealed.
    * **Data Integrity Verification:** Hashing can be used to verify that a file or message has not been tampered with during transmission or storage. By comparing the hash of the received data with the original hash, any changes can be detected.
    * **Digital Signatures:** Hashing is a crucial component of digital signatures, as we'll see in the next section.

### Digital Signatures: Authenticity and Non-Repudiation

Digital signatures are a cryptographic technique used to verify the
authenticity and integrity of digital documents or messages. They provide a
way to ensure that a message originated from a specific sender and that it has
not been altered in transit. They also offer non-repudiation, meaning the
sender cannot deny having signed the message.

  * **How Digital Signatures Work:**
    1. The sender generates a hash of the document or message they want to sign.
    2. The sender then encrypts the hash using their private key. This encrypted hash is the digital signature.
    3. The sender attaches the digital signature to the original document or message.
    4. The receiver uses the sender's public key to decrypt the digital signature, retrieving the original hash.
    5. The receiver then generates their own hash of the received document or message.
    6. The receiver compares the two hashes. If they match, it verifies that the message is authentic and has not been tampered with.
  * **Benefits of Digital Signatures:**
    * **Authentication:** Verifies the identity of the sender.
    * **Integrity:** Ensures that the message has not been altered.
    * **Non-repudiation:** Prevents the sender from denying they signed the message.
  * **Common Digital Signature Algorithms:**
    * [RSA](https://en.wikipedia.org/wiki/RSA_\(cryptosystem\)#Signing_messages)
    * [DSA (Digital Signature Algorithm)](https://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
    * [ECDSA (Elliptic Curve Digital Signature Algorithm)](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)

### Conclusion

Cryptography is a fundamental pillar of modern cybersecurity, providing the
tools to secure our data, communications, and online interactions.
Understanding the basics of encryption, hashing, and digital signatures is
essential for anyone navigating the digital landscape. As technology continues
to evolve, cryptography will play an increasingly vital role in protecting our
privacy and ensuring a secure digital future. By grasping these fundamental
concepts, you'll be better equipped to understand the security measures that
underpin our online world and make informed decisions about protecting your
own digital assets.

**Further Reading:**

  * [Cryptography](https://www.khanacademy.org/computing/computer-science/cryptography) \- Khan Academy
  * [Crypto 101](https://www.crypto101.io/)
  * [Cryptography I](https://www.coursera.org/learn/crypto) \- Coursera
  * [Applied Cryptography](https://www.udacity.com/course/applied-cryptography--cs387) \- Udacity