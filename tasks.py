# 🎯 Easy: simple accuracy
def grader_easy(preds, labels):
    correct = sum(p == l for p, l in zip(preds, labels))
    return correct / len(labels)


# ⚖️ Medium: penalize missing urgent cases more
def grader_medium(preds, labels):
    score = 0

    for p, l in zip(preds, labels):
        if p == l:
            score += 1

        # ❌ Missing urgent case = dangerous
        elif p == "not_urgent" and l == "urgent":
            score -= 1.0

        # ⚠️ False alarm (less severe)
        elif p == "urgent" and l == "not_urgent":
            score -= 0.5

    return max(0, score / len(labels))


# 🔥 Hard: strict medical penalty
def grader_hard(preds, labels):
    score = 0

    for p, l in zip(preds, labels):
        if p == l:
            score += 1
        else:
            # heavy penalty for wrong medical decision
            score -= 1.0

    return max(0, score / len(labels))