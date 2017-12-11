# CollatzCrypt by John Dorsey
A program to encrypt a numeric payload as a sequence of transformations linking it to a numeric key.


For these two rules: if even, divide by 2; if odd, multiply by 3 and add 1 - The Collatz Conjecture questions whether there is any starting number which will not reach 1. If such a number exists, it's way bigger than 2^34 -  So in this project we will assume that every number can be transformed to 1. if this assumption is incorrect, some numbers will be invalid inputs.

There are other ways to use the two Collatz operations besides selecting one based on n%2 - In my program, an operation is valid whenever it yeilds another integer. Additionally, the reversed versions of both operations can be used. By selecting only from these 4 operations, it is possible to travel from any integer to any other integer, constructing a path between them. I have not yet proven that it is always possible to construct a path which does not pass through 1.

Once a path is constructed between two positive integers, a key and a payload, it is converted to an instruction set (an ordered list of the operations used) which is the output. These instructions, together with the key, can be used to generate the payload.



My purpose for creating this project is to learn about algorithms and algorithmic complexity. When I was given an assignment in Computer Science Principles to invent my own encryption algorithm using Berkeley's "Snap!" language, I started to create a project similar to this one, but I ran out of time and submitted something else instead.

In my first tests, I used slow searches of lists. But since I started, my CS class introduced me to the idea of sorted list searches, and my rate of calculation was increased 10,000,000,000 times. That is exactly the type of thing I am interested in accomplishing in this project. I want to use the new algorithms I learn.



The code is compatible with python3 and python2 - I added python2 compatibility so that I could run it with pypy2 on windows. Moving from cPython to pypy, my program's pool generation is about 40 times faster, while the stacked solver ranges from 2 to 50 times faster.

CollatzCrypt currently uses a pygame window to draw a diagram of the solution after solving each problem.
