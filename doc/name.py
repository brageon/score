import numpy, string

ALPHABET = "abcdefghijklmnopqrstuvwxyzåäö"
ALPHA_MAP = {ch: i + 1 for i, ch in enumerate(ALPHABET)}

def string_to_numbers(s):
    return [ALPHA_MAP[ch] for ch in s.lower() if ch in ALPHA_MAP]

def string_value(s):
    return sum(string_to_numbers(s))

strings = ["Brageon",
"Biwa"
]

all_nums = []

for i, s in enumerate(strings):
    nums = string_to_numbers(s)
    all_nums.append(nums)
    print(i, s, sum(nums) % 24)

for n in all_nums:
    p = numpy.sqrt(sum(n) % 24)

print("\nRank:", round(p, 1))
