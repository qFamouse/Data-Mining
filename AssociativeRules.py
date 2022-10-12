from itertools import combinations
from itertools import chain

class AssociativeRules:
    def __init__(self, transactions):
        self.transactions = transactions

    def strace_find_associative_rules(self):
        transactions = self.transactions
        N = len(self.transactions)

        print("Transaction:")
        for t in transactions:
            print(*t)
        print()

        all_ordered_items = list(set([el for el in chain(*transactions)]))
        all_ordered_items.sort()
        print("Existing products: ")
        print(*all_ordered_items)
        print()

        max_trans_len = len(max(transactions, key=lambda x: len(x)))
        print("Maximum transaction length: ")
        print(max_trans_len)
        print()

        sub_sequences = []
        for i in range(2, max_trans_len + 1):
            sub_sequences += [list(cmb) for cmb in combinations(all_ordered_items, i)]

        associative_rules = []
        for ss in sub_sequences:
            for el in ss:
                premise = ss[::]
                premise.remove(el)
                associative_rules.append([premise, el])

        print("All possible associative rules:")
        for a in associative_rules:
            print("{} => {}".format(a[0], a[1]), end=" || ")
        print()

        valued_rules = []

        for a in associative_rules:
            premis_freq = 0
            conseq_freq = 0
            both_freq = 0
            for t in transactions:
                if all(sub_el in t for sub_el in a[0]):
                    premis_freq += 1
                if a[1] in t:
                    conseq_freq += 1
                if all(sub_el in t for sub_el in a[0]) and (a[1] in t):
                    both_freq += 1
            if premis_freq > 0 and conseq_freq > 0:
                support = both_freq / N
                confidence = both_freq / premis_freq
                lift = support / (premis_freq * conseq_freq)
                valued_rules.append([a, support, confidence, lift])

        valued_rules.sort(key=lambda x: (x[1], x[2]), reverse=True)

        for v_r in valued_rules:
            if v_r[1] >= 0.2 and v_r[2] >= 0.2:
                print("{} => {} | support = {} confidence = {}".format(v_r[0][0], v_r[0][1], v_r[1], v_r[2], v_r[3]))
