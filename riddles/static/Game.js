$(window).ready(function(){
    sea_color = '#87b7ff';
    hit_color = '#eca7bd';
    destroyed_color = "#ff7a55";
    failed_color = "#f7ffcc";
    healthy_color = "#2edc2c";
    cannot_color = "#aaaaaa";


    var myships = [];
    var otherships = [];
    var turn;
    var gamestate = 'customizing';
    var sitranslate = {'sea' : 0, 'healthy' : 1, 'hit' : 2, 'destroyed' : 3, 'failed' : 4, 'cannot' : 5};
    var istranslate = ['sea', 'healthy', 'hit', 'destroyed', 'failed', 'cannot'];
    var ictranslate = [sea_color, healthy_color, hit_color, destroyed_color, failed_color, cannot_color];
    var gamecontinues = true;


    $('.block').click(function(event){
        handleclick(event, this);
    });

    rowcol = function (event) { return [event.target.id.charAt(6), event.target.id.charAt(7)]; };
    ////Your favourite var
    var handlehit = {
        getreq : function (pos) { return pos[0] + "/" + pos[1] + "/" + "hit" },
        handle : function (data, obj) {
            if (data['result'] == 'ok') {
                otherships = translateFromDigs(data['ships']);
                turn = !turn;
                update_colors();
                if (data['gameend'] != 'go') {
                    gamecontinues = false;
                    alert('You ' + data['gameend']);
                }
                else
                    waitingToGoInterval = setInterval(waitForOpponentToGo, 400);
            }
        },
        reqpos : function (event, obj) {$.get( handlehit.getreq(rowcol(event)), function(data) {handlehit.handle(data, obj);});}
    };
    ////Your favourite var
    function handleclick(event, obj){
        if (!gamecontinues)
            return;
        t = event.target.id.charAt(0);
        pos = rowcol(event);
        if (gamestate == 'playing' && t == 'o' && otherships[pos[0]][pos[1]] == 'sea' && turn)
            handleplaying(event, obj);
        else if (gamestate == 'customizing' && t == 'm'){
            pos = rowcol(event);
            myships[pos[0]][pos[1]] = myships[pos[0]][pos[1]] == 'healthy' ? 'sea' : 'healthy';
            color = myships[pos[0]][pos[1]] == 'healthy' ? healthy_color : sea_color;
            $(obj).css('background-color', color);
        }
    }



    function startpreparing() {
        for (i = 0; i < 10; i++) {
            myships.push([]);
            for (j = 0; j < 10; j++)
                myships[i].push('sea');
        }
        for (i = 0; i < 10; i++) {
            otherships.push([]);
            for (j = 0; j < 10; j++)
                otherships[i].push('sea');
        }
    }

    showOnlyMe();
    startpreparing();


    function translateLang(ships, func){
        res = [];
        for (i = 0; i < 10; i++) {
            res.push([]);
            for (j = 0; j < 10; j++)
                res[i].push(func[ships[i][j]]);
        }
        return res;
    }
    function translateToDigs(ships){
        return translateLang(ships, sitranslate);
    }
    function translateFromDigs(ships) {
        return translateLang(ships, istranslate);
    }

    $('#submit').click(function (event) {
        ttt = [[0,0,1,1,1,0,0,1,1,0],[0,0,0,0,0,0,0,0,0,0],[0,1,0,0,1,0,0,1,0,1],[0,1,0,0,1,0,0,0,0,0],[0,1,0,0,1,0,0,1,1,0],[0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,1,0,0]]
        myships = translateFromDigs(ttt);
        turn = true;
        update_colors();
        var myEvent = {ships : translateToDigs(myships), pk: playerid };
        $.ajax({
            url: '/thejsonevent/',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(myEvent),
            dataType: 'text',
            success: function(result) {
                t = JSON.parse(result);
                alerting = t['result'] == 'ok' ? "Ok, wait for opponent" : "Your field is wrong";
                if (t['result'] == 'ok') {
                    removeButton();
                    startCheckingOpponent();
                }
                alert(alerting);
            }
        });
    });
    var checkningOpponentInterval;
    var waitingToGoInterval;
    function startCheckingOpponent() {
        checkningOpponentInterval = setInterval(opponentOneCheck, 400);
    }
    function opponentOneCheck() {
        $.get("/" + playerid + "/game" + "/testifopponentsubmitted/", function (response) {
                if (response['submitted']) {
                    gamestate = 'playing';
                    clearInterval(checkningOpponentInterval);
                    turn = response['turn'];
                    showOpponnent();
                    if (!turn)
                        waitingToGoInterval = setInterval(waitForOpponentToGo, 400);
                    alert('Start playing!' + (turn ? " Your" :"Opponent's") + " turn!");
                }
            });
    }

    function handleplaying(event, obj){
        handlehit.reqpos(event, obj);
    }

    function update_colors() {
        someships = translateToDigs(turn ? myships : otherships);
        firstlet = turn ? 'm' : 'o';
        for (i = 0; i < 10; i++) {
            for (j = 0; j < 10; j++)
                $('#' + firstlet + 'block' + i.toString() + j.toString()).css('background-color', ictranslate[someships[i][j]]);
        }
    }
    
    function waitForOpponentToGo() {
        $.get("/" + playerid + "/game" + "/testifopponentwent/", function (response) {
                if (response['went']) {
                    clearInterval(waitingToGoInterval);
                    myships = translateFromDigs(response['ships']);
                    turn = !turn;
                    update_colors();
                    if (response['gameend'] != 'go') {
                        gamecontinues = false;
                        alert('You ' + response['gameend']);
                    }
                    else
                        alert('Your turn!');
                }
            });
    }

    function showOnlyMe(){
        $('#oboard').addClass('undispoboard');
    }
    function removeButton(){
        $('#submit').addClass('undispoboard');
    }
    function showOpponnent(){
        $('#oboard').removeClass('undispoboard');
    }
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
// 5 - cannot