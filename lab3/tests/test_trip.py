import unittest
from lab3.src.trip import Trip

class TestTrip(unittest.TestCase):

    def setUp(self):
        pass

    def test_initialization(self):
        trip1 = Trip("Paris", 7)
        self.assertEqual(trip1.destination, "Paris")
        self.assertEqual(trip1.duration, 7)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()