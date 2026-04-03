from collections import defaultdict

# ----------------------------
# NODE RANKS
# ----------------------------
node_ranks = {
    "NH": 2, "HD": 10, "NC": 5,
    "DH": 1, "CN": 4, "HN": 3,
    "ND": 6, "HC": 12, "DC": 8,
    "CH": 9, "CD": 11, "DN": 7
}

# ----------------------------
# CHORD MAP
# ----------------------------
all_chords = [
    ("HD",["F#dim7","E7#9","D9","F#9","G7","Abm"]),
    ("DN",["Adim","G7#9","E9","D#9","B7","Em7"]),
    ("DC",["Cdim7","D7#9","D+","D9","CM7","Em6"]),
    ("ND",["F#dim","F7#9","C+","G13","EM","Em9"]),
    ("CN",["Ddim","G#7#9","F+","C13","EM6","Em11"]),
    ("HC",["Ddim7","F#7#9","A+","B13","DM9","Em7#5"]),
    ("CD",["Edim7","F7b5","G+","E11","BM9","Gm11"]),
    ("CH",["D#dim","C#7#9","C9+","Eb11","FM9","Bm11"]),
    ("NC",["G#dim","C7b9","B9+","Bb13","GM9","Bbm9"]),
    ("DH",["Bdim","Eb7#9","Aadd9","C11","DM/9","Fm11"]),
    ("NH",["Bdim7","D#7","Cadd9","D11","D6/9","Am11"]),
    ("HN",["A#m7b5","B7b9","Dbm9","Bb9","G6/9","Ebm9"]),

    ("HD",["Gdim","E7b5","Ab+","C#11","Badd9","F#m11"]),
    ("DN",["A#dim7","F7b9","G#+","D13","CM/9","C#m11"]),
    ("DC",["G#m7b5","G#7","Db+","Eb9","Dadd9","F#m9"]),
    ("ND",["G#dim7","D#7#9","B+","G11","BM/9","Cm7"]),
    ("CN",["A#dim","Ab7#5","A#add9","F#13","FM/9","C#m9"]),
    ("HC",["Adim7","F#7b9","E+","F11","EM9","Gm9"]),
    ("CD",["Em7b5","A7#9","D#+","G9","GM6","Dm9"]),
    ("CH",["Fdim7","Eb7#5","F#add9","E13","E6/9","G#m11"]),
    ("NC",["Bm7b5","G#9","F#+","A9","GM/9","A#m9"]),
    ("DH",["Fdim","C7#9","Eadd9","B11","A6/9","G#m9"]),
    ("NH",["C#m7b5","G#13","C#+","F9","AM/9","A#m7"]),
    ("HN",["F#m7b5","Bb7#9","G#add9","Db9","F6/9","Fm9"])
]

# Split modes
chords_mode1 = dict(all_chords[:12])
chords_mode2 = dict(all_chords[12:])

# ----------------------------
# USER INPUT
# ----------------------------
mode = input("Select A or B: ")
seq_input = input("Enter sequence: ")
sequence = seq_input.strip().split()

chords = chords_mode1 if mode == "A" else chords_mode2

# ----------------------------
# TONAL CENTER
# ----------------------------
pitch_classes = {
    0:"C", 1:"C#/Db", 2:"D", 3:"D#/Eb",
    4:"E", 5:"F", 6:"F#/Gb", 7:"G",
    8:"G#/Ab", 9:"A", 10:"A#/Bb", 11:"B"
}

def detect_key(sequence):
    total = sum(node_ranks.get(m, 0) for m in sequence)
    mod12 = total % 12

    weights = defaultdict(int)
    for m in sequence:
        rank = node_ranks.get(m, 0)
        pc = rank % 12
        weights[pc] += rank

    best_pc = max(weights, key=weights.get) if weights else 0

    return {
        "total_weight": total,
        "mod12": mod12,
        "tonal_center_pc": best_pc,
        "key": pitch_classes[best_pc]
    }

# ----------------------------
# LOVELY NGRAMS 
# ----------------------------
def norm(a, b):
    return tuple(sorted((a, b)))

bigram_aspects = {
    norm("NH","CH"):"1c", norm("HN","CN"):"1c",
    norm("HN","CD"):"2c", norm("CN","ND"):"2c",
    norm("NC","DC"):"3c", norm("DN","HD"):"3c",
    norm("DH","HC"):"6c", norm("CH","HC"):"6c",

    norm("DH","NH"):"1Ø", norm("NH","HN"):"1Ø",
    norm("DH","CH"):"2Ø", norm("ND","DN"):"2Ø",
    norm("NH","NC"):"3Ø", norm("HN","ND"):"3Ø",
    norm("DH","NC"):"4Ø", norm("HN","DN"):"4Ø", norm("NC","CH"):"4Ø",
    norm("NH","HC"):"5Ø", norm("ND","CD"):"5Ø",
    norm("NH","DC"):"6Ø", norm("CN","HD"):"6Ø",

    norm("DH","DC"):"1s", norm("HN","HD"):"1s",
    norm("NH","CN"):"2s", norm("HN","NC"):"2s", norm("HD","HC"):"2s",
    norm("DH","HD"):"3s", norm("ND","CH"):"3s", norm("NC","HD"):"3s",
    norm("NH","ND"):"4s", norm("CN","CD"):"4s",
    norm("HN","DC"):"5s", norm("CN","CH"):"5s", norm("DN","HC"):"5s",
    norm("DH","DN"):"6s", norm("NC","CD"):"6s",

    norm("CN","NC"):"1u", norm("NC","ND"):"1u", norm("CH","HD"):"1u",
    norm("DH","HN"):"2u", norm("NH","HD"):"2u", norm("ND","DC"):"2u",
    norm("HN","HC"):"3u", norm("CN","DN"):"3u", norm("DC","HD"):"3u",
    norm("CN","DC"):"4u", norm("DC","HC"):"4u", norm("DN","CH"):"4u",
    norm("DH","CD"):"5u", norm("NH","DN"):"5u",
    norm("ND","HD"):"6u", norm("DC","CH"):"6u", norm("NH","CH"):"6u",

    norm("DN","DC"):"1g", norm("DH","CN"):"1g",
    norm("CN","HC"):"2g", norm("NC","DN"):"2g",
    norm("NH","CD"):"3g", norm("HD","CD"):"3g",
    norm("NC","HC"):"4g", norm("DN","CD"):"4g",
    norm("DH","ND"):"5g", norm("DC","CD"):"5g", norm("CD","HC"):"5g",
    norm("HN","CH"):"6g", norm("ND","HC"):"6g", norm("CH","CD"):"6g",
}

love_letter = {
    "1c":"A","3c":"A","1Ø":"A","4Ø":"A",
    "1s":"P","1g":"P","2g":"P","1u":"P",
    "2c":"F","3u":"F","5u":"F","2Ø":"F","6Ø":"F",
    "2s":"E","4u":"E","6u":"E","6g":"E","6c":"E",
    "3s":"S","4s":"S","6s":"S","3Ø":"S","5Ø":"S",
    "5s":"L","2u":"L","3g":"L","4g":"L","5g":"L",
}

def trigram_to_love(trigram):
    results = []
    pairs = [(trigram[0], trigram[1]), (trigram[1], trigram[2])]

    for a, b in pairs:
        func = bigram_aspects.get(norm(a, b))
        love = love_letter.get(func)
        results.append((f"{a}-{b}", func, love))

    return results

# ----------------------------
# CHORD MAPPING
# ----------------------------
def map_sequence_to_chords(sequence):
    mapped = []
    for idx, motif in enumerate(sequence):
        chord_list = chords.get(motif)
        if not chord_list:
            mapped.append((motif, None))
            continue

        chord = chord_list[idx % len(chord_list)]
        mapped.append((motif, chord))

    return mapped

# ----------------------------
# RUN
# ----------------------------
print("\n--- CHORDS ---")
for motif, chord in map_sequence_to_chords(sequence):
    print(motif, "→", chord)

print("\n--- TONAL CENTER ---")
print(detect_key(sequence))

print("\n--- TRIGRAM ANALYSIS ---")
trigrams = [tuple(sequence[i:i+3]) for i in range(len(sequence)-2)]

for t in trigrams:
    print("\nTrigram:", "-".join(t))
    for step in trigram_to_love(t):
        print(" ", step)
