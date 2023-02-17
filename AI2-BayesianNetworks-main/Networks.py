# Max Wang 2.10.2023
# Kim AI2, Period 7

class BayesianTree:                                             # Can find probabilities in graphs with no cycles

    def __init__(self):
        self.nodes = {}                                         # Dictionary to store references to Node objects; key is a string


    def set_discretes(self, *args)  -> None:                    # Creates nodes with <discrete> field True
        for name, table in args:
            self.nodes[name] = Node(name, True, table)


    def set_conditionals(self, *args) -> None:                  # Creates nodes with <discrete> field False
        for name, table in args:
            self.nodes[name] = Node(name, False, table)


    # -------------------------------------------
    # Syntax for Constraints
    # >> {<name1>:<state1>, <name2>:<state2>...}
    # -------------------------------------------

    def get_probability(self, constraints: dict) -> float:      # Gets probability of a set of constraints
        # if len(constraints) == 1:                             # Checks if there is only one constraint and if it is discrete
        #     name = next(iter(constraints))                    # < Used for efficiency in edge case
        #     node = self.nodes[name]
        #     if node.is_discrete:
        #        return node.disc_prob[constraints[name]]

        total = 0.0                                             # Summing probabilities of all possible cases given constraints

        for case in self.get_cases(constraints):
            product = 1.0                                       # To get the probability for a case
            for ref in self.nodes.values():                     #     multiply all discrete and conditional probabilities
                product *= ref.probability_given(case)          # (mathematical justification not provided)
            total += product
        
        return total


    # -------------------------------------------
    # Syntax for State
    # >> (name, state)
    # See previous method for Constraints
    # -------------------------------------------

    def get_given_probability(self, state: tuple, constraints: dict) -> float:      # Finding probability of a state given constraints
        # node = self.nodes[state[0]]
        # if node.is_discrete:                                  # Checks if the given state is discrete
        #     return node.disc_prob[state[1]]                   # < Used for efficiency in edge case
        
        without_state = self.get_probability(constraints)       # Probability of the constraints being true
        constraints[state[0]] = state[1]
        with_state = self.get_probability(constraints)          # Probability of the constraints and the case being true

        return with_state / without_state                       # Final probability = (Successful cases)/(Total cases)
    

    def get_cases(self, constraints: dict) -> list:             # Generates all possible cases given constraints
        cases = [{}]

        for name, node in self.nodes.items():                   # Iterating over all nodes
            if name in constraints:                             # If a constraint is set, add this state to all cases
                for i in range(len(cases)):
                    cases[i][name] = constraints[name]
            
            else:
                newcases = []
                for case in cases:                              # Iterating over all cases
                    for value in node.states:                   # Iterating over all states
                        newdict = case.copy()                   # Makes copies of the case for every value
                        newdict[name] = value
                        newcases.append(newdict)
                cases = newcases
        
        return cases


class Node:

    def __init__(self, name, discrete: bool, table: list):
        self.name = name                                        
        self.is_discrete = discrete
        self.states = set()

        if self.is_discrete:
            self.disc_prob = {}                                 # If using discrete probabilites,
            for k, v in table.items():                          #     set all states to corresponding probabilities
                self.disc_prob[k] = v
                self.states.add(k)

        else:
            self.parents = table[1]                             # If using conditional probabilities,
            self.cond_prob = {}                                 #     set all conditional states to corresponding probabilities
            for k, v in table[0]:
                self.cond_prob[k] = v
                self.states.add(k[-1])


    def probability_given(self, constraints: dict) -> float:    # Return probability given a set of constraints spanning all nodes 
        if self.is_discrete:                                    # If is discrete, return discrete probability
            return self.disc_prob[constraints[self.name]]
        
        key = tuple([constraints[parent] for parent in self.parents] + [constraints[self.name]])
        return self.cond_prob[key]                              # If not discrete, return probability corresponding to parents' states