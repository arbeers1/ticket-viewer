//File: ticket_displayer.js
//Description: Link backend to frontend, Extracts ticket data
//Author: Alex Beers

function get_tickets(page_num){
    $.getJSON($SCRIPT_ROOT + '/get_tickets', {
        page: page_num
    }, function(data) {
        display_tickets(data)
    }); 
}

function display_tickets(tks){
    console.log(tks)
    for(var i = 0; i < tks.tickets.length; i++){
        $('#tv > tbody:last-child').append('<tr>'+
        '<td>' + tks.tickets[i].priority + '</td>' +
        '<td>' + tks.tickets[i].status + '</td>' + 
        '<td>' + tks.tickets[i].id + '</td>' +
        '<td>' + tks.tickets[i].subject + '</td>' +
        '<td>' + tks.tickets[i].requester_name + '</td>' +
        '<td>' + tks.tickets[i].requester_updated + '</td>' +
        '<td>' + tks.tickets[i].assignee + '</td>' +
        '</tr>');
    }
}