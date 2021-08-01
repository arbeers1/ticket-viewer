from flask import Flask, render_template, jsonify, request, session
from src.ticket_viewer import TicketViewer as tv
import os

#Start application
app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/get_tickets', methods=['GET'])
def tickets():
    tks = tv.get_tickets(request.args.get('page'))
    if(not tks[0]):
        #TODO: Return error page
       return jsonify(tickets='none', count = 'none', error=tks[1])
    
    result = []
    user_cache = []
    for x in range (len(tks[1]['tickets'])):
        result.append(tv.parse_ticket_simple(tks[1], x, user_cache))
    return jsonify(tickets = result, count = tks[1]['count'], error='none')

@app.route('/detailed')
def detailed():
    session["vis"] = True
    return render_template('ticket.html')

@app.route('/detailedinfo', methods=['GET'])
def detailed_info():
    tks = tv.get_tickets(int(request.args.get('page')))
    if(not tks[0]):
        #TODO: Return error page
        raise NotImplementedError    
    return tv.parse_ticket_detailed(tks[1], int(request.args.get('index')))
