from itertools import combinations
from itertools import chain


class AprioriAll:
    def __init__(self, actors, transactions):
        self.MIN_SUPPORT = 0.4
        self.actors = actors
        self.transactions = transactions

    def strace_result(self):
        # View input data
        print("Client transactions")
        for k in self.transactions:
            print(f"{k} : {self.transactions[k]}")
        print()

        # Choosing candidates
        candidates = self.__choosing_candidates()
        print("Choosing candidates")
        for i, s in enumerate(candidates):
            print("{} - {}".format(str(s).rjust(9), i + 1))
        print()

        # Transformation phase
        print("Transformation phase")
        transformed_transactions = self.__transformation(candidates)
        for k in transformed_transactions:
            print("{} : {}".format(k, transformed_transactions[k]))
        print()

        # Sequence generation phase
        print("Sequence generation phase")
        sub_numeric_sequences = self.__sequence_generation(candidates, transformed_transactions)
        print("All possible combinations of selected sequences")
        print(*sub_numeric_sequences)

        # Maximization phase
        print(f"Combinations of transaction sequences with current support level: {self.MIN_SUPPORT}")
        valid_transaction_sequences = self.__maximization_phase(sub_numeric_sequences, transformed_transactions)

        for k in valid_transaction_sequences:
            if valid_transaction_sequences[k] != -1:
                print("{} - {}".format(k, valid_transaction_sequences[k]))

    def __choosing_candidates(self):
        # Unique Combinations
        all_ordered_items = set()
        for k in self.actors:
            for el in self.transactions[k]:
                all_ordered_items.update(el)

        max_transaction_length = max([max([len(el) for el in self.transactions[k]]) for k in self.actors])

        unique_combinations = []
        for i in range(1, max_transaction_length + 1):
            unique_combinations += [cmb for cmb in combinations(all_ordered_items, i)]

        # Choosing candidates
        candidates = []
        min_support_count = round(self.MIN_SUPPORT * len(self.actors))
        for combination in unique_combinations:
            count = 0
            for k in self.actors:
                for el in self.transactions[k]:
                    if all((sub_el in el) for sub_el in combination):
                        count += 1
                        break
            if count >= min_support_count:
                candidates.append(combination)

        candidates.sort()
        return candidates

    def __transformation(self, candidates):
        # Init transformed
        transformed_transactions = {}
        for k in self.actors:
            transformed_transactions[k] = [[]]
        # Algorithm
        for k in self.actors:
            for t in self.transactions[k]:
                if len(transformed_transactions[k][-1]) != 0:
                    transformed_transactions[k].append([])
                for i, s in enumerate(candidates):
                    if all(sub_el in t for sub_el in s):
                        transformed_transactions[k][-1].append(i + 1)

        return transformed_transactions

    def __sequence_generation(self, candidates, transformed_transactions):
        numeric_sequences = [i + 1 for i in range(len(candidates))]
        max_transaction_length = max([len(transformed_transactions[k]) for k in transformed_transactions])

        sub_numeric_sequences = []
        for i in range(1, max_transaction_length + 1):
            sub_numeric_sequences += [cmb for cmb in combinations(numeric_sequences, i)]

        return sub_numeric_sequences

    def __maximization_phase(self, sub_numeric_sequences, transformed_transactions):
        valid_transaction_sequences = {}

        for s in sub_numeric_sequences:
            support = 0
            for k in transformed_transactions:
                flattened = list(chain(*transformed_transactions[k]))
                if all(sub_el in flattened for sub_el in s):
                    support += 1
            if support >= 2:
                valid_transaction_sequences[s] = support

        for i, k1 in enumerate(valid_transaction_sequences):
            for j, k2 in enumerate(valid_transaction_sequences):
                if j <= i:
                    continue
                if len(set(k1) | set(k2)) == max(len(k1), len(k2)):
                    valid_transaction_sequences[k1] = -1

        return valid_transaction_sequences
