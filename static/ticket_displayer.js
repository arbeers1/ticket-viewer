//File: ticket_displayer.js
//Description: Link backend to frontend, Extracts ticket data
//Author: Alex Beers

var total_pages = 0;
var curr_page = -1
var cached = false;
var page_cache = [] //This is a page cache list which will periodically update.
                    //Helps reduce load times by periodically updating the cache vs. calling api on user demand


/**
 * Calls the flask app to get the data for the desired page.
 * @param {*} page_num - page number to display, pass -2 to get current page
 * @param cahce - True or False, if True then data is stored in page_cache, otherwise display_tickets is auto called
 * @param load - True if loading the page for the first time 
 */
function get_tickets(page_num, cache, load){
    if(load && localStorage.getItem('page') !== 'undefined'){
        page_num = localStorage.getItem('page');
        curr_page = page_num;
        localStorage.setItem('page', 'undefined');
    }

    $.getJSON($SCRIPT_ROOT + '/get_tickets', {
        page: page_num
    }, function(data) {
        if(!cache){
            curr_page = page_num;
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
        get_tickets(i + 1, true, false);
    }
    setInterval(function(){
        for(var i = 0; i < total_pages; i++){
            get_tickets(i + 1, true, false);
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
    $('#load').css('visibility', 'hidden')
    $('#count').text('Total Tickets: ' + tks.count); 
    $('#page_count').text('Displaying page ' + curr_page + ' of ' + total_pages);
    $('#tv tbody').empty();
    url_extension = '/detailed'
    for(var i = 0; i < tks.tickets.length; i++){
        $('#tv > tbody:last-child').append('<tr id=' + i +
        ' onclick="go_to_detailed(' + i + ')">' +
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
    console.log(curr_page);
    if(curr_page < total_pages){
        curr_page++;
    }
    if(page_cache[curr_page - 1] !== undefined){
        display_tickets(page_cache[curr_page - 1]);
    }else{
        get_tickets(curr_page, false, false);
    }
}

/**
 * Displays the previous page of results in the table
 */
function prev(){
    console.log(curr_page);
    if(curr_page > 1){
        curr_page--;
    }
    if(page_cache[curr_page - 1] !== undefined){
        display_tickets(page_cache[curr_page - 1]);
    }else{
        get_tickets(curr_page, false, false);
    }
}

/**
 * Displays the first page of results in the table
 */
function first(){
    console.log(curr_page);
    curr_page = 1;
    if(page_cache[curr_page - 1] !== undefined){
        display_tickets(page_cache[curr_page - 1]);
    }else{
        get_tickets(curr_page, false, false);
    }
}

/**
 * Displays the last page of results in the table
 */
function last(){
    console.log(curr_page);
    curr_page = total_pages;
    if(page_cache[curr_page - 1] !== undefined){
        display_tickets(page_cache[curr_page - 1]);
    }else{
        get_tickets(curr_page, false, false);
    }
}

/**
 * Makes a request for the ticket detailed view and the needed information
 */
function go_to_detailed(id){
    localStorage.setItem('priority', $('#tv').find('tr:eq('+ id + ')').find("td:eq(0)").html());
    localStorage.setItem('status', $('#tv').find('tr:eq('+ id + ')').find("td:eq(1)").html());
    localStorage.setItem('id', $('#tv').find('tr:eq('+ id + ')').find("td:eq(2)").html());
    localStorage.setItem('subject', $('#tv').find('tr:eq('+ id + ')').find("td:eq(3)").html());
    localStorage.setItem('rn', $('#tv').find('tr:eq('+ id + ')').find("td:eq(4)").html());
    localStorage.setItem('up', $('#tv').find('tr:eq('+ id + ')').find("td:eq(5)").html());
    localStorage.setItem('assign', $('#tv').find('tr:eq('+ id + ')').find("td:eq(6)").html());
    localStorage.setItem('page', curr_page);
    localStorage.setItem('total_page', total_pages);
    localStorage.setItem('index', id);

    window.location.href = location.href + '/detailed';
}

function update_detailed(){
    console.log('here')
    $('#id').text('Viewing Ticket #' + localStorage.getItem('id'));
    $('#req').text('Requester: ' + localStorage.getItem('rn'));
    $('#ass').text('Assignee: ' + localStorage.getItem('assign'));
    $('#subject').text(localStorage.getItem('subject'));
    $('#req2').text(localStorage.getItem('rn'));

    $.getJSON($SCRIPT_ROOT + '/detailedinfo',{
        page: localStorage.getItem('page'),
        index: localStorage.getItem('index')
    }, function(data){
        $('#desc').text(data.description);
        let tags = 'Tags: ';
        for(var i = 0; i < data.tags.length; i++){
            tags += data.tags[i] + ' ';
        }
        $('#tags').text(tags);
    });
}
