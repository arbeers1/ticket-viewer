#File: app.py
#Description: Holds routing information for web app and handles request for data
#Author: Alex Beers

from flask import Flask, render_template, jsonify, request, session
from src.ticket_viewer import TicketViewer as tv
import os

#Start application
app = Flask(__name__)

@app.route('/')
def index():
    """
    Return home page
    """
    return render_template('index.html')

@app.route('/get_tickets', methods=['GET'])
def tickets():
    """
    Retrieves and returns a single page of tickets

    Paramaters:
       Page - the page number of the ticket

    Returns:
        Json containing tickets, count, and error if any
    """
    tks = tv.get_tickets(request.args.get('page'))
    if(not tks[0]):
       return jsonify(tickets='none', count = 'none', error=tks[1])
    
    result = []
    user_cache = []
    for x in range (len(tks[1]['tickets'])):
        result.append(tv.parse_ticket_simple(tks[1], x, user_cache))
    return jsonify(tickets = result, count = tks[1]['count'], error='none')

@app.route('/detailed')
def detailed():
    """
    Return detailed ticket view page
    """
    return render_template('ticket.html')

@app.route('/detailedinfo', methods=['GET'])
def detailed_info():
    """
    Retrieves and returns a single ticket's description and tags

    Paramaters:
        Page - the page number of the ticket
        Index - the index of the ticket to parse on the page

    Returns:
        Json containing ticket results and error if any
    """
    tks = tv.get_tickets(int(request.args.get('page')))
    if(not tks[0]):
        return jsonify(main='none', error=tks[1])    
    return jsonify(main=tv.parse_ticket_detailed(tks[1], int(request.args.get('index'))), error='none')
