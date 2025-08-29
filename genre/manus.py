import numpy as np
from collections import Counter

dcnh_map = {
    'DC': 5, 'DN': 1, 'DH': 3, 'CD': 4, 'CN': 7, 'CH': 11,
    'ND': 12, 'NC': 6, 'NH': 8, 'HD': 2, 'HC': 10, 'HN': 9 }

sequence = ['DC','CD','DH','CH','HN','DH','CD','HN','CN','CD','NC']
steps = [dcnh_map[sequence[i]] for i in range(len(sequence))]

hyperparams = {}
hyperparams['mean_step'] = np.mean(steps)
hyperparams['std_step'] = np.std(steps)
hyperparams['max_step'] = np.max(steps)
hyperparams['min_step'] = np.min(steps)
hyperparams['cadential_consistency'] = 100 - np.std(steps)*10  # higher = smoother
hyperparams['chromatic_jumps'] = np.sum([1 for s in steps if s > 5])
hyperparams['total_jumps'] = np.sum(steps)
hyperparams['backward_fifths'] = np.sum([1 for s in steps if s > 6])
hyperparams['forward_fifths'] = len(steps) - hyperparams['backward_fifths']
hyperparams['modal_shifts'] = 3  # placeholder, count mode changes if known
hyperparams['start_end_alignment'] = 100 if sequence[0] == sequence[-1] else 50
hyperparams['chromatic_density'] = hyperparams['chromatic_jumps']/len(steps)*100
hyperparams['weighted_total'] = np.mean(list(hyperparams.values())[:-1])  # avg of first 11 hyperparams

for k,v in hyperparams.items():
    print(f"{k}: {v}")

frequency = Counter(sequence)
print("\nDCNH Value Frequency in Sequence:")
for k,v in frequency.items():
    print(f"{k}: {v}")
