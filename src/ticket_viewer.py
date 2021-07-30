#File: ticket_viewer.py
#Description: Retrieve zendesk ticket details attached to an account
#Author: Alex Beers

from datetime import datetime, timezone
import json
import requests
from . import config

class TicketViewer():
    
    def get_tickets(page):
        """
        Retrieves a page of 25 tickets associated with the zendesk account ordered by date.

        Paramaters
            page - the page number to retrieve
        
        Returns
            If operation is successful:
            (True, json of 25 tickets)
            If operation fails:
            (False, displayable error string)
        """
        try:
            response = requests.get(
                url= 'https://zcctreehugger.zendesk.com/api/v2/tickets.json',
                auth=('arbeers@wisc.edu', config.passw),
                params={'sort_by': 'created_at', 'per_page': 25, 'page': page},
                timeout=60)
        except ConnectionError:
            return (False, "An error has been encountered with the network :(")
        except TimeoutError:
            return (False, "Failed to retrieve a response from the server :(")

        if(response.status_code >= 200 and response.status_code < 300):
            return (True, response.json())
        else:
            return (False, "An error has been encountered:\n" + str(response.status_code) + "\n" + response.reason)

    def parse_ticket_simple(ticket_json, index):
        """
        Parses json ticket to strip of undesired data and convert user ids and time to usable format.
        This method is intended to only return data useful for displaying tickets in a list. For more in depth 
        information on individual tickets, use parse_ticket_detailed().

        Paramaters
            ticket_json - A single page json as returned by get_tickets()
            index - The index ticket to parse

        Returns
            json with the following key/value pairs:
            priority: string, status: string, id: int, subject: string, requester_name: string, requester_updated: string, assignee: name 

        Throws
            LookupError if user name look up fails
        """

        tickets = ticket_json['tickets']

        requester_name = TicketViewer._user_name(tickets[index]['requester_id'])
        if(requester_name[0]):
            requester_name = requester_name[1]
        else:
            raise LookupError(requester_name[1])

        assignee_name = TicketViewer._user_name(tickets[index]['assignee_id'])
        if(assignee_name[0]):
            assignee_name = assignee_name[1]
        else:
            raise LookupError(assignee_name[1])

        priority = 'normal' if tickets[index]['priority'] == None else tickets[index]['priority']

        json_to_return = '''{"priority":"'''  + priority + '''",
            "status":"''' + tickets[index]['status'] + '''",
            "id":''' + str(tickets[index]['id']) + ''',
            "subject":"''' + tickets[index]['subject'] + '''",
            "requester_name":"''' + requester_name + '''",
            "requester_updated":"''' + TicketViewer._time_delta(tickets[index]['updated_at']) + '''",
            "assignee_name":"''' + assignee_name + '"}'
        return json.loads(json_to_return)
            
    def parse_ticket_detailed(ticket_json, index):
        """
        Parses json ticket list and provides information useful for when the user wants more information on an indivual ticket.
        This method only returns description and tags, meaning it is recommended that simple_parse value is stored for a full 
        ticket display.

        Paramaters
            ticket_json - A single page json as returned by get_tickets()
            index - The index ticket to parse

        Returns
            json with key/value pairs:
            tags: [tag1, tag2, ...], description: string
        """    
        tickets = ticket_json['tickets']
        tags_s = json.dumps(tickets[index]['tags'])
        json_to_return = '{"tags":' + tags_s + ',"description":"' + tickets[index]['description'] + '"}'

        return json.loads(json_to_return, strict=False)

    def _user_name(user_id):
        """
        Helper method for parsing tickets to retrieve the displayed user's name from an id.

        Paramaters
            user_id - an integer id number associated with a user

        Returns
            If operation is successful:
            (True, user_name)
            If operation fails:
            (False, displayable error string)

        """
        try:
            response = requests.get(
                url= 'https://zcctreehugger.zendesk.com/api/v2/users/' + str(user_id),
                auth=('arbeers@wisc.edu', config.passw),
                timeout=60)
        except ConnectionError:
            return (False, "An error has been encountered with the network :(")
        except TimeoutError:
            return (False, "Failed to retrieve a response from the server :(")

        #Return username if api call successful
        if(response.status_code >= 200 and response.status_code < 300):
            return (True, response.json()['user']['name'])
        else:
            return (False, "An error has been encountered:\n" + str(response.status_code) + "\n" + response.reason)

    def _time_delta(time):
        """
        Helper method to find the time difference since ticket last updated.

        Paramaters
            time - the utc time string as returned by the get_tickets() json

        Returns
            string with time difference
        """
        orig_time = datetime(int(time[0:4]), int(time[5:7]), int(time[8:10]), int(time[11:13]),
                                      int(time[14:16]), int(time[17:19]), tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - orig_time
        if(delta.days > 0):
            return str(delta.days) + ' day(s) ago'
        else:
            return str(int(delta.seconds/3600)) + ' hour(s) ago'
