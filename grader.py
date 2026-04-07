class MedicalGrader:
    def __init__(self):
        self.total = 0
        self.correct = 0

    def grade(self, true_label: str, predicted_label: str):
        """
        Compare true vs predicted label

        Args:
            true_label (str): actual label (urgent / not_urgent)
            predicted_label (str): model prediction
        """
        self.total += 1

        if true_label == predicted_label:
            self.correct += 1
            return 1.0
        else:
            return 0.0

    def accuracy(self):
        if self.total == 0:
            return 0.0
        return self.correct / self.total