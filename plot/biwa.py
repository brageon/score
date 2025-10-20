import numpy as np
from collections import Counter

fifths_map = {
    'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5,
    'F#': 6, 'C#': 7, 'G#': 8, 'D#': 9, 'A#': 10, 'F': 11,
    'Gb': 6, 'Db': 7, 'Ab': 8, 'Eb': 9, 'Bb': 10,
    'Cm': 0, 'Gm': 1, 'Dm': 2, 'Am': 3, 'Em': 4, 'Bm': 5,
    'F#m': 6, 'C#m': 7, 'G#m': 8, 'D#m': 9, 'A#m': 10, 'Fm': 11,
    'Cdim': 0, 'Gdim': 1, 'Ddim': 2, 'Adim': 3, 'Edim': 4, 'Bdim': 5,
    'F#dim': 6, 'C#dim': 7, 'G#dim': 8, 'D#dim': 9, 'A#dim': 10, 'Fdim': 11
}

user_input = input("Enter chords: ")
sequence = user_input.strip().split()

steps = [fifths_map[ch] for ch in sequence if ch in fifths_map]

hyperparams = {}
hyperparams['mean_step'] = np.mean(steps)
hyperparams['std_step'] = np.std(steps)
hyperparams['max_step'] = np.max(steps)
hyperparams['min_step'] = np.min(steps)
hyperparams['cadential_consistency'] = 100 - np.std(steps) * 10
hyperparams['chromatic_jumps'] = np.sum([1 for s in steps if s > 5])
hyperparams['total_jumps'] = np.sum(steps)
hyperparams['backward_fifths'] = np.sum([1 for s in steps if s > 6])
hyperparams['forward_fifths'] = len(steps) - hyperparams['backward_fifths']
hyperparams['start_end_alignment'] = 100 if sequence[0] == sequence[-1] else 50
hyperparams['chromatic_density'] = hyperparams['chromatic_jumps'] / len(steps) * 100
hyperparams['weighted_total'] = np.mean(list(hyperparams.values())[:-1])

for k, v in hyperparams.items():
    print(f"{k}: {v}")

frequency = Counter(sequence)
print("\nChords Counted:")
for k, v in frequency.items():
    print(f"{k}: {v}")
