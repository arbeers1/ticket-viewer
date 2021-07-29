#File: ticket_tests.py
#Descritption: Testing methods for ticket_viewer
#Author: Alex Beers

import unittest
import sys
sys.path[0] = sys.path[0].replace('tests', 'src')
from ticket_viewer import TicketViewer as tv

class TestTicketRetrieval(unittest.TestCase):

    def test_get_tickets(self):
        """
        Test ensures that a json list is retrieved containing 2 pages, total 101 tickets.
        """
        result = tv.get_tickets()
        self.assertTrue(result[0])
        self.assertEqual(result[1][0]['count'], 101)
        self.assertEqual(len(result[1]), 2)
        self.assertEqual(len(result[1][0]['tickets']), 100)
        self.assertEqual(len(result[1][1]['tickets']), 1)

if __name__ == '__main__':
    unittest.main()
