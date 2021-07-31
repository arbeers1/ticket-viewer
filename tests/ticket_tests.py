#File: ticket_tests.py
#Descritption: Testing methods for ticket_viewer
#Author: Alex Beers

import unittest
from datetime import datetime
import sys
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
        cache = []
        result = tv._user_name(1265123600889, cache)
        self.assertTrue(result[0])
        self.assertEqual(result[1], 'Alex Beers')

        result = tv._user_name(1265063393490, cache)
        self.assertTrue(result[0])
        self.assertEqual(result[1], 'The Customer')

        result = tv._user_name(-1, cache)
        self.assertFalse(result[0])

    def test_simple_parse(self):
        """
        Test the simple ticket parse
        """
        result = tv.get_tickets(1)
        assert(result[0])
        list = []
        result = tv.parse_ticket_simple(result[1], 0, user_cache = list)
        self.assertEqual(result['priority'], 'normal')
        self.assertEqual(result['status'], 'open')
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['subject'], 'Sample ticket: Meet the ticket')
        self.assertEqual(result['requester_name'], 'The Customer')
        self.assertTrue('day' in result['requester_updated'])
        self.assertEqual(result['assignee_name'], 'Alex Beers')
        
    def test_detailed_parse(self):
        """
        Test the detailed ticket parse
        """
        result = tv.get_tickets(1)
        assert(result[0])
        result = tv.parse_ticket_detailed(result[1], 0)
        self.assertEqual(len(result['tags']), 3)
        self.assertEqual(result['tags'][0], 'sample')
        self.assertTrue('learn more' in result['description'])
       

if __name__ == '__main__':
    unittest.main()
