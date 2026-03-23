# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import math


FRAGMENTS = [
    ("I1", 9, [0.06, 0.85, 0.23, -0.88]),
    ("I2", 15, [0.23, 0.78, 0.68, 0.34]),
    ("I3", 15, [0.66, 0.17, 0.48, 0.29]),
    ("I4", 10, [1.23, -0.36, 1.09, 0.05]),
    ("I5", 7, [-0.37, 0.62, 0.61, -0.46]),
    ("I6", 12, [0.97, 0.16, 1.25, -0.25]),
    ("I7", 17, [0.4, 0.98, -0.06, 1.37]),
    ("I8", 8, [1.13, 1.29, -0.2, -0.22]),
    ("I9", 6, [0.47, 0.67, 0.34, 0.36]),
    ("I10", 13, [-0.06, 0.68, -0.39, 0.21]),
    ("I11", 8, [0.45, -0.28, 0.95, 0.77]),
    ("I12", 8, [0.42, 1.09, 0.09, 1.2]),
    ("I13", 12, [0.88, 0.95, 0.39, 0.04]),
    ("I14", 12, [0.58, 1.31, 0.55, 0.23]),
    ("I15", 10, [0.98, 1.36, 0.18, -0.16]),
    ("I16", 13, [0.22, 1.08, 0.33, -0.4]),
    ("I17", 5, [0.76, -0.23, 0.21, -0.13]),
    ("I18", 9, [-0.39, 0.94, 0.97, 0.38]),
    ("I19", 16, [0.92, 0.8, 1.45, 0.07]),
    ("I20", 15, [0.39, 0.43, 1.33, 0.9]),
    ("I21", 6, [-0.12, -0.39, 0.17, 0.13]),
]

PAIR_BONUSES = {
    ("I7", "I10"): -0.57,
    ("I10", "I13"): -0.35,
    ("I7", "I11"): 0.67,
    ("I7", "I15"): -0.53,
    ("I3", "I11"): 0.03,
    ("I6", "I10"): -0.32,
    ("I4", "I7"): -0.18,
    ("I7", "I14"): 0.14,
    ("I18", "I21"): -0.59,
    ("I1", "I11"): 0.59,
    ("I1", "I5"): -0.14,
    ("I10", "I14"): 0.31,
    ("I6", "I11"): -0.38,
    ("I10", "I19"): -0.15,
    ("I13", "I19"): -0.41,
    ("I11", "I14"): 0.39,
    ("I1", "I19"): 0.45,
    ("I12", "I18"): 0.61,
    ("I8", "I11"): -0.35,
    ("I13", "I15"): 0.55,
    ("I1", "I7"): -0.02,
    ("I12", "I19"): -0.49,
    ("I17", "I20"): 0.4,
    ("I3", "I8"): 0.54,
    ("I1", "I21"): 0.35,
    ("I12", "I16"): -0.23,
    ("I7", "I8"): 0.04,
    ("I4", "I20"): -0.33,
    ("I2", "I21"): -0.38,
    ("I8", "I18"): -0.53,
    ("I5", "I14"): -0.38,
    ("I11", "I21"): 0.15,
    ("I8", "I21"): -0.29,
    ("I8", "I20"): 0.61,
    ("I6", "I20"): -0.62,
    ("I6", "I21"): -0.55,
    ("I2", "I14"): -0.55,
    ("I14", "I19"): 0.56,
    ("I14", "I15"): 0.68,
    ("I2", "I4"): 0.59,
    ("I9", "I18"): 0.09,
    ("I9", "I20"): 0.21,
    ("I5", "I7"): -0.13,
    ("I16", "I18"): 0.5,
    ("I1", "I8"): 0.41,
}

BASE_LOGITS = [-2.37, -0.68, -2.48, 0.03]


def logit_to_percent(logit: float) -> float:
    return 100.0 / (1.0 + math.exp(-logit))


def enumerate_half(frags, id_lookup):
    internal_pairs = []
    for (a, b), bonus in PAIR_BONUSES.items():
        if a in id_lookup and b in id_lookup:
            internal_pairs.append((id_lookup[a], id_lookup[b], bonus))

    subsets = []
    n = len(frags)
    for mask in range(1 << n):
        wc = 0
        sums = [0.0, 0.0, 0.0, 0.0]
        chosen_ids = []
        for i, (frag_id, frag_wc, frag_scores) in enumerate(frags):
            if (mask >> i) & 1:
                wc += frag_wc
                chosen_ids.append(frag_id)
                for m in range(4):
                    sums[m] += frag_scores[m]

        pair_bonus = 0.0
        for i, j, bonus in internal_pairs:
            if ((mask >> i) & 1) and ((mask >> j) & 1):
                pair_bonus += bonus

        subsets.append((mask, wc, [x + pair_bonus for x in sums], chosen_ids))
    return subsets


def solve():
    left = FRAGMENTS[:10]
    right = FRAGMENTS[10:]
    left_ids = {frag_id: i for i, (frag_id, _, _) in enumerate(left)}
    right_ids = {frag_id: i for i, (frag_id, _, _) in enumerate(right)}

    left_subsets = enumerate_half(left, left_ids)
    right_subsets = enumerate_half(right, right_ids)

    cross_pairs = []
    for (a, b), bonus in PAIR_BONUSES.items():
        if a in left_ids and b in right_ids:
            cross_pairs.append((left_ids[a], right_ids[b], bonus))
        elif b in left_ids and a in right_ids:
            cross_pairs.append((left_ids[b], right_ids[a], bonus))

    best = None
    for lmask, lwc, lsums, lids in left_subsets:
        for rmask, rwc, rsums, rids in right_subsets:
            wc = lwc + rwc
            if best is not None and wc >= best[0]:
                continue

            cross_bonus = 0.0
            for li, ri, bonus in cross_pairs:
                if ((lmask >> li) & 1) and ((rmask >> ri) & 1):
                    cross_bonus += bonus

            logits = [BASE_LOGITS[m] + lsums[m] + rsums[m] + cross_bonus for m in range(4)]
            probs = [logit_to_percent(x) for x in logits]
            mean = sum(probs) / 4.0
            floor = min(probs)

            if mean >= 97.0 and floor >= 92.0:
                chosen = sorted(lids + rids, key=lambda s: int(s[1:]))
                best = (wc, chosen, mean, floor)

    if best is None:
        raise RuntimeError("No valid solution found.")
    return best


def main() -> None:
    wc, chosen, mean, floor = solve()
    answer = f"{','.join(chosen)};{wc};{mean:.2f}%;{floor:.2f}%"
    print(answer)


if __name__ == "__main__":
    main()
