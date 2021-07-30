#File: ticket_viewer.py
#Description: Retrieve zendesk ticket details attached to an account
#Author: Alex Beers

from datetime import timezone
import requests
import datetime
import config

class TicketViewer():
    
    def get_tickets():
        """
        Retrieves a list of tickets associated with the zendesk account.

        Paramaters
            None
        
        Returns
            If operation is successful:
            (True, [json page 1, json page 2, ...]) where each json page has a max of 100 tickets
            If operation fails:
            (False, displayable error string)
        """
        url_to_get = 'https://zcctreehugger.zendesk.com/api/v2/tickets.json'
        final_result = []
        #Loop through each page
        while(True):
            try:
                response = requests.get(
                    url= url_to_get,
                    auth=('arbeers@wisc.edu', config.passw),
                    params={'sort_by': 'created_at'},
                    timeout=60)
            except ConnectionError:
                return (False, "An error has been encountered with the network :(")
            except TimeoutError:
                return (False, "Failed to retrieve a response from the server :(")

            #Append response if api call is successful
            if(response.status_code >= 200 and response.status_code < 300):
                response = response.json()
                final_result.append(response)
                #Exit loop if no more pages are left, otherwise continue to the next page
                if(response['next_page'] == None):
                    break 
                else:
                    url_to_get = response['next_page']
            else:
                return (False, "An error has been encountered:\n" + str(response.status_code) + "\n" + response.reason)
        return(True, final_result)

    def parse_tickets_simple(ticket_json, start_index, end_index=None):
        """
        Parses json ticket list and provides simple information about an individual ticket or a range of tickets.
        This method is intended to only return data useful for displaying tickets in a list. For more in depth 
        information on individual tickets, use parse_tickets_detailed().

        Paramaters
            ticket_json - A single page json as returned by get_tickets()
            start_index - The index ticket to start parsing
            end_index - (Optional) If provided method will parse between start/end index
                                   Otherwise method will only parse start_index

        Returns
            [(ticket_details_1), (ticket_details2), ...]
            where each ticket_details_n is a tuple formatted (priority, status, id, subject, requester, requester_updated, assignee)

        Throws
            ValueError if start/end index is not in range 0-99
            IndexError if provided index is out of bounds of the provided json 'tickets' array
            LookupError if user name look up fails
        """
        if(end_index == None):
            end_index = start_index + 1
        if(start_index < 0 or start_index > 99 or end_index < 0 or end_index > 99):
            raise ValueError("Index is out of page boundries")

        tickets = ticket_json['tickets']
        final_list = []
        for x in range(start_index, end_index):
            priority = tickets[x]['priority']
            status = tickets[x]['status']
            id = tickets[x]['id']
            subject = tickets[x]['subject']
            requester_name = TicketViewer._user_name(tickets[x]['requester_id'])
            if(requester_name[0]):
                requester_name = requester_name[1]
            else:
                raise LookupError(requester_name[1])
            time = TicketViewer._time_delta(tickets[x]['updated_at'])
            assignee_name = TicketViewer._user_name(tickets[x]['assignee_id'])
            if(assignee_name[0]):
                assignee_name = assignee_name[1]
            else:
                raise LookupError(assignee_name[1])
            final_list.append((priority, status, id, subject, requester_name, time, assignee_name))
        return final_list
            
                 

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
        orig_time = datetime.datetime(int(time[0:4]), int(time[5:7]), int(time[8:10]), int(time[11:13]),
                                      int(time[14:16]), int(time[17:19]), tzinfo=timezone.utc)
        delta = datetime.datetime.now(timezone.utc) - orig_time
        if(delta.days > 0):
            return str(delta.days) + ' day(s) ago'
        else:
            return str(int(delta.seconds/3600)) + ' hour(s) ago'
