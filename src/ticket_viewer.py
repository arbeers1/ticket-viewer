#File: ticket_viewer.py
#Description: Retrieve zendesk ticket details attached to an account
#Author: Alex Beers

import requests
import config

class TicketViewer():
    
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
        try:
            response = requests.get(
                url='https://zcctreehugger.zendesk.com/api/v2/tickets.json',
                auth=('arbeers@wisc.edu', config.passw),
                timeout=60)
        except ConnectionError:
            return (False, "An error has been encountered with the network :(")
        except TimeoutError:
            return (False, "Failed to retrieve a response from the server :(")

        #Validate response
        if(response.status_code >= 200 and response.status_code < 300):
            return (True, response.json())
        else:
            return (False, "An error has been encountered:\n" + str(response.status_code) + "\n" + response.reason)

