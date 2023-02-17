# Max Wang 2.10.2023
# Kim AI2, Period 7

# Tester code for Bayesian Trees, for Probability Mini-Unit Day 4 Pop Quiz

from Networks import *

def main():

    # -----------------------------------------------------------------
    # Syntax for Discrete Probabilities
    # >> (<name>, {<case1>:<probability1>, <case2>:<probability2>...})
    # -----------------------------------------------------------------

    # -----------------------------------------------------------------
    # Syntax for Conditional Probabilities
    # >> (<name>, (<probabilities>, <parents>))
    #
    # parents (string names): [<parent1>, <parent2>...]
    # probabilities: [((<parent1>, <parent2>... <case1>), <chance>),
    #                 ((<parent1>, <parent2>... <case2>), <chance>),
    #                ...]
    # -----------------------------------------------------------------

    Burglary = ("B", {True:0.001, False:0.999})         # Discrete Probabilities of Burglary
    Earthquake = ("E", {True:0.002, False:0.998})       # Discrete Probabilities of Earthquake
    
    Alarm_Parents = ["B", "E"]
    Alarm_Problt = [((True, True, True), 0.95),
                    ((True, True, False), 0.05),
                    ((True, False, True), 0.94),
                    ((True, False, False), 0.06),
                    ((False, True, True), 0.29),
                    ((False, True, False), 0.71),
                    ((False, False, True), 0.001),
                    ((False, False, False), 0.999)]
    Alarm = ("A", (Alarm_Problt, Alarm_Parents))        # Conditional Probabilities of Alarm

    JC_Parents = ["A"]
    JC_Problt = [((True, True), 0.90),
                 ((True, False), 0.10),
                 ((False, True), 0.05),
                 ((False, False), 0.95)]
    JohnCalls = ("J", (JC_Problt, JC_Parents))          # Conditional Probabilities of JohnCalls

    MC_Parents = ["A"]
    MC_Problt = [((True, True), 0.70),
                 ((True, False), 0.30),
                 ((False, True), 0.01),
                 ((False, False), 0.99)]
    MaryCalls = ("M", (MC_Problt, MC_Parents))          # Conditional Probabilities of MaryCalls

    model = BayesianTree()                                                      # Create Bayesian Network
    model.set_discretes(Burglary, Earthquake)                                   # Add discrete nodes
    model.set_conditionals(Alarm, JohnCalls, MaryCalls)                         # Add conditional nodes

    print(model.get_probability({"B":False}))                                   # Odds of Burglary = False
    print(model.get_given_probability(("A", False), {"B":True, "E":False}))     # Odds of Alarm = False, given Burglary = True & Earthquake = True
    print(model.get_given_probability(("B", True), {"J":True, "M":True}))       # Odds of Burglary = True, given JohnCalls = True & MaryCalls = True

    
if __name__ == "__main__":                              # Only executes main() if this file is the one being ran 
    main()                                              # If this file is imported, main() will not run
