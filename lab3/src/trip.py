class Trip:

    def __init__(self,destination,duration):
        self.participants = []
        self.destination = destination
        self.duration = duration

    def calculate_cost(self):
        return self.duration * 100

    def add_participant(self, participant):
        if participant == "":
            raise ValueError("Participant name cannot be empty")
        self.participants.append(participant)