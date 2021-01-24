# Cryptid

Cryptid is a simple game pitting intelligent agents against one another for survival. The game consists of a board of variable size on which _Cryptids_ move around and attack one another.

An example of the game looks like the following:
```
*----------*
|     R    |
|      A RR|
| T       R|
|   A      |
|T  TR TT  |
|          |
|T  RAA    |
| AT    R  |
|TR TR A  A|
|T R    AAA|
*----------*
RandomCryptid: 10  Triffid: 10  Afanc: 10 
```
The game board is a 10x10 grid, and each space is either empty or occupied by a Cryptid object. Each Cryptid object implements a `getMove` function - and one "round" of the game consists of the program running the game calling `getMove` on each and every Cryptid, and updating the game state appropriately.
The valid moves for a Cryptid are `LEFT`, `RIGHT`, `HOP` and `INFECT`, which result in a Cryptid turning left or right, moving forward if possible, or attacking a Cryptid in front and turning it into its own Cryptid.

The game is won when one Cryptid class is the only Cryptid class left standing.

The goal of the _players_ in this case is to design a winning `getMove` function for their Cryptid.

# References
 This game is basically a stripped-down port of a programming assignment from CSE 142 at the University of Washington, "Critter", which is written in Java.


