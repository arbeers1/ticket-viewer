//File: ticket_displayer.js
//Description: Link backend to frontend, Extracts ticket data
//Author: Alex Beers

/**
 * Calls the flask app to get the data for the desired page.
 * @param {*} page_num - page number to display
 */
var total_pages = 0;
var curr_page = -1;

function get_tickets(page_num){
    if(page_num == 1){
        $("#prev").attr("disabled","disabled");
    }else{
        $("#prev").removeAttr("disabled");
    }
    if(page_num == total_pages){
        $("#next").attr("disabled","disabled");
    }else{
        $("#next").removeAttr("disabled");
    }
    $.getJSON($SCRIPT_ROOT + '/get_tickets', {
        page: page_num
    }, function(data) {
        curr_page = page_num;
        display_tickets(data);
    }); 
}

/**
 * Displays the tickets to the table
 * @param {*} tks - The json returned from Flask's get_tickets call
 */
function display_tickets(tks){
    $('#count').text('Total Tickets: ' + tks.count);
    total_pages = Math.ceil(tks.count / 25); 
    $('#page_count').text('Displaying page ' + curr_page + ' of ' + total_pages);
    $('#tv tbody').empty();
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

/**
 * Displays the next page of results in the table
 */
function next(){
    get_tickets(curr_page + 1);
}

/**
 * Displays the previous page of results in the table
 */
function prev(){
    get_tickets(curr_page - 1);
}

/**
 * Displays the first page of results in the table
 */
function first(){
   get_tickets(1);
}

/**
 * Displays the last page of results in the table
 */
function last(){
    get_tickets(total_pages);
}
