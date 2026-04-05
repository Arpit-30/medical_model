def grader_easy(preds, labels):
    correct = sum(p == l for p, l in zip(preds, labels))
    return correct / len(labels)


def grader_medium(preds, labels):
    score = 0
    for p, l in zip(preds, labels):
        if p == l:
            score += 1
        elif p == "spam" and l == "not_spam":
            score -= 0.5
    return max(0, score / len(labels))


def grader_hard(preds, labels):
    score = 0
    for p, l in zip(preds, labels):
        if p == l:
            score += 1
        else:
            score -= 1
    return max(0, score / len(labels))