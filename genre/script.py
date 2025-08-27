import numpy as np

# Map each note/chord root to its Circle of Fifths position (C=0, G=1, D=2, ...)
fifths_map = {
    'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'F#': 6, 'C#': 7,
    'Ab': 8, 'Eb': 9, 'Bb': 10, 'F': 11 }

# Example runes / chords (use roots only)
sequence = ['G', 'F#', 'A', 'E', 'D', 'C#', 'E', 'B', 'F#', 'E', 'F#', 'C#', 'F#', 'E', 'B']

# Compute step distances in fifths
steps = [abs(fifths_map[sequence[i]] - fifths_map[sequence[i+1]]) % 12 for i in range(len(sequence)-1)]

# A Mixolydian, B Aeolian, C Ionian, D Dorian, E Phrygian, F# Lydian
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
    print(f"{k}: 
    {v}")
