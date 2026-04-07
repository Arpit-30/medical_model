"""
Medical Triage Client (Simple Prediction Client)
"""

from server.email_env_environment import MedicalModel


class MedicalClient:
    def __init__(self):
        self.model = MedicalModel()

    def predict(self, symptoms: str):
        """
        Predict urgency from symptoms

        Args:
            symptoms (str): Patient symptoms text

        Returns:
            dict: urgency + message
        """
        return self.model.predict(symptoms)


# ✅ Example usage
if __name__ == "__main__":
    client = MedicalClient()

    while True:
        text = input("\nEnter symptoms: ")
        result = client.predict(text)

        print(f"Urgency: {result['urgency']}")
        print(f"Message: {result['message']}")