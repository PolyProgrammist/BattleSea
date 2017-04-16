$(window).ready(function(){
    untouched_color = '#87b7ff';
    hit_color = '#eca7bd';
    destroy_color = "#ff7a55";
    fail_color = "#f7ffcc";

    $('.block').click(function(event){
        if($(this).attr('killed') != 1) {
            $(this).attr('killed', '1');
        }
        else{
            $(this).attr('killed', '2');
        }
        //reqpos(event, this);
        console.log(playerid);
        $.get(playerid + '/showid/', function (data) {
            console.log(data['temp']);
            console.log(data);
        });
    });
    rowcol = function (event) { return [event.target.id.charAt(5), event.target.id.charAt(6)]; };
    getreq = function (pos) { return pos[0] + "/" + pos[1] + "/" + "hit" };
    reqpos = function (event, obj) {$.get( getreq(rowcol(event)), function(data) {handle(data, obj);});};

    handle = function (data, obj) {
        $(obj).css('background-color', destroy_color);
    };
});