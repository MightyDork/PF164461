class Trip:

    def __init__(self,destination,duration):
        self.destination = destination
        self.duration = duration

    def calculate_cost(self):
        return self.duration * 100