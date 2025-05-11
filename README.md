# Discrete Logarithm Problem Algorithms

Course presentation for MA532 Mathematical Cryptography.

## Overview

Implementation of four algorithms for solving the Discrete Logarithm Problem:
- **Linear Search** - O(n) time, O(1) space
- **Baby-step Giant-step** - O(√n) time, O(√n) space
- **Pohlig-Hellman** - Efficient for smooth group orders
- **Pollard's Rho** - O(√n) time, O(1) space (probabilistic)

## Results
![image](https://github.com/user-attachments/assets/eabe5eb0-90a8-4607-b7cd-328812dda73e)


## Running the Code

```bash
python main.py
```

Tests all algorithms on primes of various sizes and displays performance comparisons.

## Files

- `main.py` - Driver program
- `utils.py` - Algorithm implementations  
- `crypto_ppt_draft1.pdf` - Presentation slides
- `ppt_tex.tex` - LaTeX source for presentation
- `cryptography_3_discrete_logarithms_in_cryptography.pdf` - Lecture notes
- `LectureNotes9.pdf` - Additional reference material

## Results

The program tests algorithms on small (101), medium (9,973), and large (104,729) primes, providing execution times and success rates.

## Author

Ved Umrajkar  
Department of Mathematics  
Indian Institute of Technology, Roorkee
