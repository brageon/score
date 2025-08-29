import numpy as np
from collections import Counter

# Map each note/chord root to its Circle of Fifths position (C=0, G=1, D=2, ...)
fifths_map = {
    'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'Gb': 6, 'Db': 7,
    'Ab': 8, 'Eb': 9, 'Bb': 10, 'F': 11 }

# The first four sales nodes are DC HN CH CD. 
sequence = ['C','G','F','Eb','D','Eb','G','D','F','G','A','C']
steps = [fifths_map[sequence[i]] for i in range(len(sequence))]

hyperparams = {}
hyperparams['mean_step'] = np.mean(steps)
hyperparams['std_step'] = np.std(steps)
hyperparams['max_step'] = np.max(steps)
hyperparams['min_step'] = np.min(steps)
hyperparams['cadential_consistency'] = 100 - np.std(steps)*10
hyperparams['chromatic_jumps'] = np.sum([1 for s in steps if s > 5])
hyperparams['total_jumps'] = np.sum(steps)
hyperparams['backward_fifths'] = np.sum([1 for s in steps if s > 6])
hyperparams['forward_fifths'] = len(steps) - hyperparams['backward_fifths']
hyperparams['start_end_alignment'] = 100 if sequence[0] == sequence[-1] else 50
hyperparams['chromatic_density'] = hyperparams['chromatic_jumps']/len(steps)*100
hyperparams['weighted_total'] = np.mean(list(hyperparams.values())[:-1])

for k,v in hyperparams.items():
    print(f"{k}: {v}")

frequency = Counter(sequence)
print("\nChord Frequency:")
for k,v in frequency.items():
    print(f"{k}: {v}")
