# Decrypting Cipher with Markov Chain Monte Carlo

## Abstract
*We examine the use of Markov Chain Monte Carlo (MCMC) algorithm to break subsitution ciphers. We use MCMC to sample keys from possible decryption keys. We employ n-gram frequency analysis to evaluate the quality of the sampled keys. We use simulated annealing to enhance the performance of algorithm. The accuracy of the algorithm is almost 100% for the cipher text with length of 1000 or more characters. For shorter cipher text, the accuracy depends on the length of the n-gram used in the n-gram frequency analysis.*
## Introduction
Markov Chain Monte Carlo are popular methods of sampling from a complicated probability distributions. Its use in cryptography is not new. This approach was first introduced by Marc Coram and Phil Beinke, and later studied more systematically by Connor. In this project, we implement these techniques using Python. We first introduce subsitution ciphers, and then describe the MCMC algorithm. We then describe the n-gram frequency analysis, and finally we describe the simulated annealing algorithm. We then present the results of our experiments.

## Subsitution Ciphers
A subsitution cipher is a type of encryption algorithm that replaces each plaintext character with a different ciphertext character. The original text is called the plain text and the encrypted text is called cipher text. In substitution ciphers, the encryption key is a permutation of the alphabet. For example, we could replace A with B, B with C, C with D and so on. For this example, the shift would be 1. With this key, the world 'hello' becomes 'ifmmp'. Such substitution ciphers where characters are shifted by an integer are called Caeser ciphers. Instead of shifting, we could also randomly permute the alphabet. For example, we could replace A with C, B with D, C with E and so on. With this key, the world 'hello' becomes 'jgnnq'. Such substitution ciphers where characters are randomly permuted are called random ciphers.
#### Python Implementation
In the file *cipher.py*, we have implemented the substitution ciphers as a class. The substitution cipher takes a key of permutation of alphabets, like 'UNMLFPRITKQSDBOAYCZVWHJXEG'. The subsitution cipher is inherited by the Caeser cipher and the random cipher. Caeser cipher takes an integer as a key instead of the alphabets. Giving it a key of 1 would shift all the alphabets by 1, like A becomes B, B becomes C, Z becomes A and so on. The random cipher doesn't take any input. It will just randomly permute the alphabets and use it as a key. These all classes have two main methods: *encrypt* and *decrypt*. *encrypt* takes a string as input and returns the cipher text. *decrypt* takes a cipher text as input and returns the plain text. 
## Markov Chain Monte Carlo
Markov Chain Monte Carlo is an algorithm to sample from a complicated probability distribution. The state space in our project is the state of all possible decryption keys. It has $$26!$$ possible states. The transition probability is the probability of moving from one state to another. In our project, we use the transition probability of randomly swapping two characters in the key. The initial state is a random key. The goal is to sample from the distribution of the keys that decrypt the cipher text. We use the n-gram frequency analysis to evaluate the quality of the sampled keys. The n-gram frequency analysis is described in the next section. We use simulated annealing to enhance the performance of algorithm. The simulated annealing is described in the next section as well.
## n-gram Frequency Analysis
We read a large text in English to do the frequency analysis. Such a text is called reference text. We use *War and Peace* as our reference text. We then count the frequency of each n-gram in the reference text. For example, if we use n=2, we would count the frequency of each pair of characters. We then use the frequency of each n-gram in the reference text to evaluate the quality of the sampled keys. We use the log-likelihood of the n-gram frequency in the reference text and the n-gram frequency in the cipher text. The likelihood is defined as:
$$\pi(x)=\Pi_{\beta_1 \beta_2} r(\beta_1,\beta_2)^{f_x(\beta_1,\beta_2)}$$
where, $$r(\beta_1,\beta_2)$$ is the frequency of the n-gram $$\beta_1\beta_2$$ in the reference text, $$f_x(\beta_1,\beta_2)$$ is the frequency of the n-gram $$\beta_1\beta_2$$ in the cipher text, and $$\pi(x)$$ is the likelihood of the key $$x$$. We use the log-likelihood instead of the likelihood because it is easier to compare the log-likelihood of different keys.
## Simulated Annealing
Simulated annealing is a technique to enhance the performance of MCMC algorithm. It is a technique to control the randomness of the algorithm. The idea is to start with a high temperature, and then slowly decrease the temperature. The randomness of the algorithm is controlled by the temperature. The higher the temperature, the more random the algorithm is. The lower the temperature, the less random the algorithm is. 
## Algorithm
The algorithm is as follows:
1. Initialize the temperature to a high value.
2. Initialize the current state to a random key.
3. Initialize the best state to the current state.
4. While the temperature is not low enough:
    1. Generate a new state by randomly swapping two characters in the current state.
    2. If the new state has a higher log-likelihood than the current state, then set the current state to the new state.
    3. If the new state has a higher log-likelihood than the best state, then set the best state to the new state.
    4. Otherwise, set the current state to the new state with probability $$e^{\frac{L(x')-L(x)}{T}}$$, where $$L(x)$$ is the log-likelihood of the current state, $$L(x')$$ is the log-likelihood of the new state, and $$T$$ is the temperature.
    5. Decrease the temperature.
5. Return the best state.
##### References
 - [1] [Markov Chain Monte Carlo](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo)
 - [2] [DecipherArt](http://probability.ca/jeff/ftpdir/decipherart.pdf)
 - [3] [Data Structures and Algorithms in Python](https://www.amazon.com/Structures-Algorithms-Python-Michael-Goodrich/dp/1118290275)
 - [4] [S. Connor (2003): Simulation and Solving Substituion Codes](https://www-users.york.ac.uk/~sbc502/decode.pdf)