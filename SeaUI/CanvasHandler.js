f = function () {

    var canvas = document.getElementById("me_canvas");
    canvas.width = 1000;
    canvas.height = 500;
    var ctx = canvas.getContext("2d");

    var squarewidth;
    var fieldsize;

    function start() {
        var tab = 20;
        var wd = (canvas.width - (4 * tab)) / 2;
        drawField(tab, 0, wd);
        drawField(3 * tab + wd, 0, wd);
        drawFire(tab + 3 * squarewidth, 5 * squarewidth);
    }

    function drawField(x, y, wd) {
        ctx.fillStyle = "#87b7ff";
        ctx.fillRect(x, y, wd, wd);
        fieldsize = 10;
        squarewidth = wd / (fieldsize + 1);
        drawLines(x, y, wd, true);
        drawLines(x, y, wd, false);
        t = squarewidth / 4;
        insertLetters(t + x, -t + y + 2 * squarewidth, true);
        insertLetters(t + x + squarewidth, -t + y + squarewidth, false);
    }

    function drawLn(x1, y1, x2, y2) {
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
    }

    function drawLines(x, y, wd, hor) {
        for (i = 0; i < fieldsize + 2; i++) {
            drawLn(x, y, x + wd * hor, y + wd * !hor);
            y += squarewidth * hor;
            x += squarewidth * !hor;
        }
        ctx.stroke()
    }

    function insertLetters(x, y, hor) {
        ctx.fillStyle = "#FFFFFF";
        ctx.font = "30px Arial"
        var c = hor ? 'A'.charCodeAt(0) : '0'.charCodeAt(0);
        for (i = 0; i < fieldsize; i++) {
            ctx.fillText(String.fromCharCode(c), x, y);
            y += squarewidth * hor;
            x += squarewidth * !hor;
            c++;
        }
    }

    function drawFire(x, y) {
        var logoImg = new Image();
            logoImg.onload = function () {
                ctx.drawImage(logoImg, x, y, squarewidth, squarewidth);
            }
            logoImg.src = "fire.png";
    }


    start();
}