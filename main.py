from AprioriAll import AprioriAll

actors = [1, 2, 3, 4, 5]

transactions = {
    1: [[30], [90]],
    2: [[10, 20], [30], [40, 60, 70]],
    3: [[30, 50, 70]],
    4: [[30], [40, 70], [90]],
    5: [[90]]
}

apriori_all = AprioriAll(actors, transactions)
apriori_all.strace_result()
