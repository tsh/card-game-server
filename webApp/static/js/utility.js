var Colors = {
    RED: "#F00",
    GREEN: "#7CFC00",
    stopGREEN: "#c6ff90",
    stopRED: "#ffa2a2"
}

var Utility = {
    drawFavicon: function(color){
        /*Рисует фавикон отображающий подключение к серверу*/
        var canvas = document.createElement('canvas');
        canvas.width = 32;
        canvas.height = 32;
        var ctx = canvas.getContext('2d');
        var grd=ctx.createRadialGradient(16,16,2,16,16,16);
        /* цвет центра круга, на основании этого устанавливаем грани окружности*/
        grd.addColorStop(0,color);
        if (color === Colors.GREEN){
            grd.addColorStop(1,Colors.stopGREEN);
        } else {
            grd.addColorStop(1,Colors.stopRED);
        }

        ctx.fillStyle=grd;
        ctx.beginPath();
        ctx.arc(16,16,16,0,2*Math.PI);
        ctx.fill();
        /*создать из рисунка фавикон, и установить его*/
        var link = document.createElement('link');
        link.type = 'image/x-icon';
        link.rel = 'shortcut icon';
        link.href = canvas.toDataURL("image/x-icon");
        document.getElementsByTagName('head')[0].appendChild(link);
    }
}
