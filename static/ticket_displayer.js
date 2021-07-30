//File: ticket_displayer.js
//Description: Script for displaying tickets to the end user
//Author: Alexander Beers

/**
 * Builds the HTML list of tickets, provided a list of tickets
 * 
 * @param - list, a list of simple view tickets obtained from ticket_viewer.py 
 */
function display_ticket_list(){
    console.log(data)
    for(var i = 0; i < data.length; i++){
        $('#tv > tbody:last-child').append('<tr>' + 
        '<td>' + data[i][0] + '</td>' +
        '<td>' + data[i][1] + '</td>' +
        '<td>' + data[i][2] + '</td>' +
        '<td>' + data[i][3] + '</td>' +
        '<td>' + data[i][4] + '</td>' +
        '<td>' + data[i][5] + '</td>' +
        '<td>' + data[i][6] + '</td>' +
        '</tr>');
    }
}