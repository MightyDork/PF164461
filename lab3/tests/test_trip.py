import unittest
from lab3.src.trip import Trip

class TestTrip(unittest.TestCase):

    def setUp(self):
        pass

    def test_initialization(self):
        trip1 = Trip("Paris", 7)
        self.assertEqual(trip1.destination, "Paris")
        self.assertEqual(trip1.duration, 7)

    def test_calculate_cost(self):
        trip1 = Trip("Paris", 7)
        self.assertEqual(trip1.calculate_cost(),700)
        trip2 = Trip("Rome", 5)
        self.assertEqual(trip2.calculate_cost(),500)

    def test_add_participant(self):
        trip1 = Trip("Paris", 7)
        trip1.add_participant("John")
        self.assertIn(self, "John", trip1.participants)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()