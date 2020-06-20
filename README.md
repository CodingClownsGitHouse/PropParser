# Parser for Propositional formulae
This program builds a parse tree for given formulae. 

A formula is well formed, if the tree builds successfully. The accepted grammar is:
```
PL:= P | F | (PL -> PL) 
```
Where 
- PL is the set of formula in propositional logic
- P is the set of propositional variables
- F is Falsum (always False)
- -> is the implication

The repo contains test data. You can test the program by running:
```shell script
cat test_data/valid.txt | python prop_parser.py
```