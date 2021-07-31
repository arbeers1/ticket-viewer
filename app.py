from flask import Flask, render_template, jsonify, request
from src.ticket_viewer import TicketViewer as tv
from src import config

#Start application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_tickets', methods=['GET'])
def tickets():
    print('here')
    tks = tv.get_tickets(request.args.get('page'))
    if(not tks[0]):
        #TODO: Return error page
        raise NotImplementedError
    
    result = []
    for x in range (len(tks[1]['tickets'])):
        result.append(tv.parse_ticket_simple(tks[1], x))
    print('return tickets')
    return jsonify(tickets = result)