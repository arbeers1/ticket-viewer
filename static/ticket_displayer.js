//File: ticket_displayer.js
//Description: Link backend to frontend, Extracts ticket data
//Author: Alex Beers

var total_pages = 0;
var curr_page = -1;
var cached = false;
var page_cache = [] //This is a page cache list which will periodically update.
                    //Helps reduce load times by periodically updating the cache vs. calling api on user demand


/**
 * Calls the flask app to get the data for the desired page.
 * @param {*} page_num - page number to display
 * @param cahce - True or False, if True then data is stored in page_cache, otherwise display_tickets is auto called
 */
function get_tickets(page_num, cache){
    $.getJSON($SCRIPT_ROOT + '/get_tickets', {
        page: page_num
    }, function(data) {
        curr_page = page_num;
        if(!cache){
            display_tickets(data);
        }else{
            console.log('cached');
            page_cache[page_num - 1] = data;
        }
    }); 
}

/**
 * Caches tickets every 10 seconds into page_cache
 */
function cache_tickets(){
    cached = !cached;
    for(var i = 0; i < total_pages; i++){
        get_tickets(i + 1, true);
    }
    setInterval(function(){
        for(var i = 0; i < total_pages; i++){
            get_tickets(i + 1, true);
        }
    }, 10000)
}

/**
 * Displays the tickets to the table
 * @param {*} tks - The json returned from Flask's get_tickets call
 */
function display_tickets(tks){
    total_pages = Math.ceil(tks.count / 25);
    if(!cached) {cache_tickets();}
    if(curr_page == 1){
        $("#prev").attr("disabled","disabled");
    }else{
        $("#prev").removeAttr("disabled");
    }
    if(curr_page == total_pages){
        $("#next").attr("disabled","disabled");
    }else{
        $("#next").removeAttr("disabled");
    }
    $('#count').text('Total Tickets: ' + tks.count); 
    $('#page_count').text('Displaying page ' + curr_page + ' of ' + total_pages);
    $('#tv tbody').empty();
    url_extension = '/detailed'
    for(var i = 0; i < tks.tickets.length; i++){
        $('#tv > tbody:last-child').append('<tr onclick="go_to_detailed()"> '+
        '<td>' + tks.tickets[i].priority + '</td>' +
        '<td>' + tks.tickets[i].status + '</td>' + 
        '<td>' + tks.tickets[i].id + '</td>' +
        '<td>' + tks.tickets[i].subject + '</td>' +
        '<td>' + tks.tickets[i].requester_name + '</td>' +
        '<td>' + tks.tickets[i].requester_updated + '</td>' +
        '<td>' + tks.tickets[i].assignee_name + '</td>' +
        '</tr>');
    }
}

/**
 * Displays the next page of results in the table
 */
function next(){
    if(curr_page < total_pages){
        curr_page++;
    }
    if(page_cache[curr_page - 1] !== undefined){
        display_tickets(page_cache[curr_page - 1]);
    }else{
        get_tickets(curr_page, false);
    }
}

/**
 * Displays the previous page of results in the table
 */
function prev(){
    if(curr_page > 1){
        curr_page--;
    }
    if(page_cache[curr_page - 1] !== undefined){
        display_tickets(page_cache[curr_page - 1]);
    }else{
        get_tickets(curr_page, false);
    }
}

/**
 * Displays the first page of results in the table
 */
function first(){
    curr_page = 1;
    if(page_cache[curr_page - 1] !== undefined){
        display_tickets(page_cache[curr_page - 1]);
    }else{
        get_tickets(curr_page, false);
    }
}

/**
 * Displays the last page of results in the table
 */
function last(){
    curr_page = total_pages;
    if(page_cache[curr_page - 1] !== undefined){
        display_tickets(page_cache[curr_page - 1]);
    }else{
        get_tickets(curr_page, false);
    }
}

/**
 * Makes a request for the ticket detailed view and the needed information
 */
function go_to_detailed(){
    console.log('here');
    location.href = location.href + '/detailed';
}
