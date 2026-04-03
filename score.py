import re

# --- Fifths ---
ENHARMONIC = {
    'Bb': 'A#', 'Cb': 'B', 'Db': 'C#', 'Eb': 'D#', 'Fb': 'E',
    'Gb': 'F#', 'Ab': 'G#'
}
CIRCLE = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F']

# --- Exotic Chords ---
CHORD_SETS = {
    "DH":["Bdim","Eb7#9","Aadd9","C11","DM/9","Fm11","Fdim","C7#9","Eadd9","B11","A6/9","G#m9"],
}

# --- Parser ---
CHORD_RE = re.compile(r'^([A-G](?:b|#)?)([^/]*)?(?:/([A-G](?:b|#)?))?$')

def normalize_note(note):
    note = note.capitalize()
    return ENHARMONIC.get(note, note)

def parse_chord(chord):
    m = CHORD_RE.match(chord.strip())
    if not m:
        return None, None, None
    root = normalize_note(m.group(1))
    quality = m.group(2) or ""
    bass = normalize_note(m.group(3)) if m.group(3) else None
    return root, quality, bass

# --- Compute Path ---
def nfc_steps(chords, base):
    b = CIRCLE.index(normalize_note(base))
    path = []
    colors = []
    for c in chords:
        root, quality, _ = parse_chord(c)
        if root not in CIRCLE:
            continue
        idx = CIRCLE.index(root)
        step = (idx - b) % 12
        path.append(step)
        colors.append(chord_tension_score(quality))
    return path, colors

# --- Tension Score ---
def chord_tension_score(quality):
    score = 0
    if 'dim' in quality: score += 2
    if 'aug' in quality or '+' in quality: score += 2
    if 'b5' in quality or '#5' in quality: score += 2
    if 'b9' in quality or '#9' in quality: score += 2
    if '11' in quality: score += 2
    if '13' in quality: score += 3
    if 'M9' in quality or '6/9' in quality: score -= 1
    return max(score,0)

# --- Detect Harmony ---
def detect_tritone_subs(path):
    return [(i, i+1) for i in range(len(path)-1) if abs(path[i+1]-path[i])==6]

def detect_coltrane_cycles(path):
    cycles = []
    for i in range(len(path)-2):
        a,b,c = path[i:i+3]
        if (b-a)%12==4 and (c-b)%12==4:
            cycles.append((i,i+1,i+2))
    return cycles

def functional_vector(path):
    vec = []
    for p in path:
        if p==0: vec.append("T")
        elif p<=2: vec.append("S")
        elif p<=5: vec.append("D")
        elif p==6: vec.append("TT")
        else: vec.append("X")
    return vec

# --- Music Parameters ---
def jazz_density(colors):
    return round((sum(colors)/(len(colors) or 1))*2)

def score_tritone_usage(path):
    return round((len(detect_tritone_subs(path))/(len(path) or 1))*10)

def score_coltrane_complexity(path):
    return round((len(detect_coltrane_cycles(path))/(len(path) or 1))*10)

def score_functional_clarity(path):
    vec = functional_vector(path)
    clarity = sum(1 for v in vec if v in ("T","S","D"))
    return round((clarity/(len(vec) or 1))*9 + 1)

# --- Genre-Independent Musical Parameters ---
def score_rhythmic_variation(path):
    diffs = [abs(path[i+1]-path[i]) for i in range(len(path)-1)]
    return round(min(sum(diffs)/(len(diffs) or 1)*2, 10))

def score_voice_leading(path):
    diffs = [abs(path[i+1]-path[i]) for i in range(len(path)-1)]
    small_steps = sum(1 for d in diffs if d<=2)
    return round((small_steps/(len(diffs) or 1))*10)

def score_modal_mixture(path):
    return round((len(set(p%7 for p in path))/(len(path) or 1))*10)

def score_melodic_leaps(path):
    diffs = [abs(path[i+1]-path[i]) for i in range(len(path)-1)]
    leaps = sum(1 for d in diffs if d>=5)
    return round((leaps/(len(diffs) or 1))*10)

def score_chord_repetition(path):
    repeats = sum(1 for i,p in enumerate(path) if p in path[:i])
    return round((repeats/(len(path) or 1))*10)

def score_harmonic_density(path):
    return round((len([p for p in path if p!=0])/(len(path) or 1))*10)

# --- Main ---
def main():
    base = input("Base key: ").strip() or 'C'
    choice = input("Chord set: ").strip().upper()

    if choice in CHORD_SETS:
        chords = CHORD_SETS[choice]
    else:
        chords = choice.split()

    path, colors = nfc_steps(chords, base)

    print("\nFunctional Flow:", " ".join(functional_vector(path)))
    print("Tritone Subs:", detect_tritone_subs(path))
    print("Coltrane Cycles:", detect_coltrane_cycles(path))
    print("NFC Path:", [round(p,2) for p in path])
    print("Jazz Density:", jazz_density(colors))

    scores = {
        "Jazz Density": jazz_density(colors),
        "Tritone Usage": score_tritone_usage(path),
        "Coltrane Complexity": score_coltrane_complexity(path),
        "Functional Clarity": score_functional_clarity(path),
        "Rhythmic Variation": score_rhythmic_variation(path),
        "Voice Leading": score_voice_leading(path),
        "Modal Mixture": score_modal_mixture(path),
        "Melodic Leaps": score_melodic_leaps(path),
        "Chord Repetition": score_chord_repetition(path),
        "Harmonic Density": score_harmonic_density(path)
    }

    print("\n--- Scorecard ---")
    for k,v in scores.items():
        print(f"{k:20s}: {v}")

    avg = (sum(scores.values())/len(scores))/len(scores)
    print(f"\nCoherence: {avg:.2f}")

if __name__=="__main__":
    main()
