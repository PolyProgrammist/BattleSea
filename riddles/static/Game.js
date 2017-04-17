$(window).ready(function(){
    sea_color = '#87b7ff';
    hit_color = '#eca7bd';
    destroyed_color = "#ff7a55";
    failed_color = "#f7ffcc";
    healthy_color = "#2edc2c";

    $('.block').click(function(event){
        handleclick(event, this);
    });

    rowcol = function (event) { return [event.target.id.charAt(6), event.target.id.charAt(7)]; };

    var handlehit = {
        getreq : function (pos) { return pos[0] + "/" + pos[1] + "/" + "hit" },
        handle : function (data, obj) {
            $(obj).css('background-color', destroyed_color);
        },
        reqpos : function (event, obj) {$.get( handlehit.getreq(rowcol(event)), function(data) {handlehit.handle(data, obj);});}
    };

    function handleclick(event, obj){
        t = event.target.id.charAt(0);
        if (gamestate == 'playing' && t == 'o')
            handlehit.reqpos(event, obj);
        else if (gamestate == 'customizing' && t == 'm'){
            pos = rowcol(event);
            ships[pos[0]][pos[1]] = ships[pos[0]][pos[1]] == 'healthy' ? 'sea' : 'healthy';
            color = ships[pos[0]][pos[1]] == 'healthy' ? healthy_color : sea_color;
            $(obj).css('background-color', color);
        }
    }

    var ships = [];
    var gamestate = 'customizing';
    var sitranslate = {'sea' : 0, 'healthy' : 1, 'hit' : 2, 'destroyed' : 3, 'failed' : 4};
    var istranslate = ['sea', 'healthy', 'hit', 'destroyed', 'failed'];
    function startpreparing() {
        for (i = 0; i < 10; i++) {
            ships.push([]);
            for (j = 0; j < 10; j++)
                ships[i].push('sea');
        }
    }

    startpreparing();

    function translateToDigs(ships){
        res = [];
        for (i = 0; i < 10; i++) {
            res.push([]);
            for (j = 0; j < 10; j++)
                res[i].push(sitranslate[ships[i][j]]);
        }
        return res;
    }

    $('#submit').click(function (event) {
        var myEvent = {ships : translateToDigs(ships) };
        console.log(JSON.stringify(myEvent));
        $.ajax({
            url: '/thejsonevent/',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(myEvent),
            dataType: 'text',
            success: function(result) {
                t = JSON.parse(result);
                alert(t['result']);
            }
        });
    });

});
// handle
// 0 - customizing
// 1 - playing
// blocks
// 0 - sea
// 1 - healthy
// 2 - hit
// 3 - destroyed
// 4 - failed