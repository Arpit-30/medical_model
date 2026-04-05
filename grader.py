from models import Action

class EmailGrader:
    def __init__(self):
        self.total = 0
        self.correct = 0

    def grade(self, true_label, action: Action):
        self.total += 1

        if action.action_type == true_label:
            self.correct += 1
            return 1.0
        else:
            return 0.0

    def final_score(self):
        if self.total == 0:
            return 0.0
        return self.correct / self.total