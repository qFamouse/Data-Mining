from AprioriAll import AprioriAll
from AssociativeRules import AssociativeRules

apriori_all_actors = [1, 2, 3, 4, 5]

apriori_all_transactions = {
    1: [[30], [90]],
    2: [[10, 20], [30], [40, 60, 70]],
    3: [[30, 50, 70]],
    4: [[30], [40, 70], [90]],
    5: [[90]]
}

associative_rules_transactions = [
    ["A", "B", "C"],
    ["A", "C", "D"],
    ["B", "C", "D"],
    ["A", "D", "E"],
    ["B", "C", "E"]
]


# apriori_all = AprioriAll(actors, apriori_all_transactions)
# apriori_all.strace_result()

associative_rules = AssociativeRules(associative_rules_transactions)
associative_rules.strace_find_associative_rules()