#File: ticket_tests.py
#Descritption: Testing methods for ticket_viewer
#Author: Alex Beers

import unittest
import sys
sys.path[0] = sys.path[0].replace('tests', 'src')
from ticket_viewer import TicketViewer as tv

class TestTicketRetrieval(unittest.TestCase):

    def test_get_tickets(self):
        result = tv.get_tickets()
        self.assertTrue(result[0])
        self.assertEqual(result[1]['count'], 101)

if __name__ == '__main__':
    unittest.main()
