import json
from flask import Flask, render_template, jsonify
from ticket_viewer import TicketViewer as tv

simple_list = [] #Holds information on tickets to display in a list, where each element is a parse_ticket_simple() list
#Start application
app = Flask(__name__)

@app.route('/')
def index():
    response = tv.get_tickets()
    if(not response[0]): 
        #TODO: return error
        return render_template('index.html') 
    
    total_count = response[1][0]['count']
    remainder = 100 if total_count % 100 == 0 else total_count % 100
    for x in range(len(response[1])):
        if(len(response[1]) <  len(response[1]) - 1):
            simple_list.extend(tv.parse_tickets_simple(response[1][x], 0, 100))
        else:
            simple_list.extend(tv.parse_tickets_simple(response[1][x], 0, remainder))
    data = jsonify(tickets=simple_list)

    return render_template('index.html', simple = data)