#File: ticket_tests.py
#Descritption: Testing methods for ticket_viewer
#Author: Alex Beers

import unittest
from datetime import datetime
import sys
import json
sys.path[0] = sys.path[0].replace('tests', 'src')
from ticket_viewer import TicketViewer as tv

class TestTicketRetrieval(unittest.TestCase):

    def test_get_tickets(self):
        """
        Test retrieving tickets.
        """
        result = tv.get_tickets(1)
        self.assertTrue(result[0])
        self.assertEqual(result[1]['count'], 101)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        self.assertEqual(len(result[1]['tickets']), 25)
        result = tv.get_tickets(5)
        self.assertEqual(len(result[1]['tickets']), 1)

    def test_time_delta(self):
        """
        Test the helper method _time_delta() to ensure an accurate delta is returned
        """
        result = tv._time_delta("2021-07-20T20:29:47Z")
        self.assertTrue('day' in result)

        time = datetime.utcnow()
        self.assertEqual('0 hour(s) ago', tv._time_delta(str(time)))

    def test_user_lookup(self):
        """
        Test the help method _user_name() 
        """
        result = tv._user_name(1265123600889)
        self.assertTrue(result[0])
        self.assertEqual(result[1], 'Alex Beers')

        result = tv._user_name(1265063393490)
        self.assertTrue(result[0])
        self.assertEqual(result[1], 'The Customer')

        result = tv._user_name(-1)
        self.assertFalse(result[0])

    def test_simple_parse_individual(self):
        """
        Test the simple ticket parse (one ticket)
        """
        
    def test_simple_parse_multiple(self):
        """
        Test the simple ticket parse (multiple tickets)
        """
       

    def test_simple_parse_errors_raised(self):
        """
        Test that the appropriate errors are raised in simple parse
        """
        
    def test_detailed_parse_errors_raised(self):
        """
        Test that the appropriate errors are raised in detailed parse
        """
       

if __name__ == '__main__':
    unittest.main()
