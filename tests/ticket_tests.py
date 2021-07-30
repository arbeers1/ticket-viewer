#File: ticket_tests.py
#Descritption: Testing methods for ticket_viewer
#Author: Alex Beers

import unittest
from datetime import datetime
import sys
from unittest.suite import TestSuite
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

    def test_time_delta(self):
        """
        Test the helper method _time_delta() to ensure an accurate delta is returned
        """
        result = tv._time_delta("2021-07-20T20:29:47Z")
        self.assertTrue('day' in result)
        self.assertTrue(int(result[0:1]) > 5)

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
        result = tv.get_tickets()
        assert(result[0] == True)
        parse = tv.parse_tickets_simple(result[1][0], 0)
        self.assertEqual(len(parse), 1)
        self.assertEqual(parse[0][0], 'normal')
        self.assertEqual(parse[0][1], 'open')
        self.assertEqual(parse[0][2], 1)
        self.assertEqual(parse[0][3], 'Sample ticket: Meet the ticket')
        self.assertEqual(parse[0][4], 'The Customer')
        self.assertTrue('day' in parse[0][5])
        self.assertEqual(parse[0][6], 'Alex Beers')

    def test_simple_parse_multiple(self):
        """
        Test the simple ticket parse (multiple tickets)
        """
        result = tv.get_tickets()
        assert(result[0] == True)
        parse = tv.parse_tickets_simple(result[1][0], 0, end_index=5)
        self.assertEqual(len(parse), 5)
        for x in parse:
            self.assertTrue(parse[0][2] < 7)

    def test_simple_parse_errors_raised(self):
        """
        Test that the appropriate errors are raised in simple parse
        """
        result = tv.get_tickets()
        with(self.assertRaises(ValueError)):
            tv.parse_tickets_simple(result[1][0], 90, end_index=110)
        with(self.assertRaises(ValueError)):
            tv.parse_tickets_simple(result[1][0], 110)

        with(self.assertRaises(IndexError)):
            tv.parse_tickets_simple(result[1][1], 0, 5)

    def test_detailed_parse(self):
        """
        Test detailed ticket return
        """
        result = tv.get_tickets()
        assert(result[0] == True)
        parse = tv.parse_ticket_detailed(result[1][0], 0)
        self.assertEqual(len(parse), 9)
        self.assertEqual(parse[0], 'normal')
        self.assertEqual(parse[1], 'open')
        self.assertEqual(parse[2], 1)
        self.assertEqual(parse[3], 'The Customer')
        self.assertEqual(parse[4], 'Alex Beers')
        self.assertEqual(len(parse[5]), 3)
        self.assertEqual(parse[6], 'Sample ticket: Meet the ticket')
        self.assertTrue('day' in parse[8])

    def test_detailed_parse_errors_raised(self):
        """
        Test that the appropriate errors are raised in detailed parse
        """
        result = tv.get_tickets()
        with(self.assertRaises(ValueError)):
            tv.parse_ticket_detailed(result[1][0], 110)
        with(self.assertRaises(ValueError)):
            tv.parse_ticket_detailed(result[1][0], -1)

        with(self.assertRaises(IndexError)):
            tv.parse_ticket_detailed(result[1][1], 5)

if __name__ == '__main__':
    unittest.main()
