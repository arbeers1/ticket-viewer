#File: ticket_viewer.py
#Description: Retrieve zendesk ticket details attached to an account
#Author: Alex Beers

import requests
import config

class TicketViewer():
    
    #TODO: Get information from all possible ticket pages and return it in a list of pages, make page size 25
    def get_tickets():
        """
        Retrieves a list of tickets associated with the zendesk account.

        Paramaters
            None
        
        Returns
            If operation is successful:
            (True, json result)
            If operation fails:
            (False, displayable error string)
        """
        url_to_get = 'https://zcctreehugger.zendesk.com/api/v2/tickets.json'
        final_result = []
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

