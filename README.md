# 02180_belief_revision_agent

## Introduction
This project is a belief revision engine designed to revise an agent's beliefs based on a given input propositional formula. The engine is implemented in the form of a sequence of stages and supports propositional logic in its symbolic form.

### Group Members
- Lucas Sandby
- Steven Tran
- Rolando Esquivel-Sancho
- Daniel Emil Wiinberg

## Stages of the Belief Revision Engine
The belief revision engine is implemented in four stages:

1. **Belief Base Design and Implementation:** The belief base is designed and implemented to store the agent's beliefs.
2. **Logical Entailment Checking Method:** A method for checking logical entailment is implemented using resolution-based techniques without relying on any existing packages.
3. **Contraction of Belief Base:** The belief base is contracted based on a priority order on formulas in the belief base.
4. **Expansion of Belief Base:** The belief base is expanded based on the agent's new beliefs.

## Requirements
To use the symbolic representation, install Sympy by running the following command:
```bash
pip install sympy 
```

### Execution

1. To run the AGM postulates, execute:
```bash
python postulates.py
```

2. To run the Test-Cases execute:
```bash
python unitTest.py
```

3. To use the belief base, configure the  `list_of_beliefs` and `alpha` in  `main.py`

Example:
```bash
list_of_beliefs = [A&B,A] 
alpha = (B)
```

