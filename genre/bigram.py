from collections import defaultdict

node_ranks = {
    "NH": 2, "HD": 10, "NC": 5,
    "DH": 1, "CN": 4, "HN": 3,
    "ND": 6, "HC": 12, "DC": 8,
    "CH": 9, "CD": 11, "DN": 7
}

def detect_intention_modes(sequence):
    positions = defaultdict(list)
    for idx, motif in enumerate(sequence):
        positions[motif].append(idx)

    motif_gaps = []
    for motif, pos_list in positions.items():
        if len(pos_list) < 2:
            continue  # skip motifs that appear only once
        # compute consecutive gaps
        gaps = [pos_list[i+1] - pos_list[i] for i in range(len(pos_list)-1)]
        shortest_gap = min(gaps)
        motif_gaps.append((motif, shortest_gap, len(pos_list)))

    motif_gaps_sorted = sorted(motif_gaps, key=lambda x: x[1])
    return motif_gaps_sorted

sequence = ["HD", "NH", "CN", "DN", "CD", "HC", "NC", "CH", "HN", "NC", "DN"]

intention_modes = detect_intention_modes(sequence)

print("Intentions (shortest recurrence gap first):")
for motif, gap, count in intention_modes:
    print(f"{motif}: shortest gap = {gap}, occurrences = {count}")

total_rank = sum(node_ranks.get(m, 0) for m in sequence)
avg = round(total_rank / len(sequence), 1)
mod_rank = total_rank % 24

print(f"Expectation: {mod_rank}, {total_rank}, {avg}")
