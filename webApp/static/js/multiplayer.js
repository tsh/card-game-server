var multiplayer = {
/*
Обьект сетевого подключения.
*/
    init: function(address){
        /*
         @param address адрес сервера для подключения по ws протоколу.
        * */
        this.webSocketHost = address;
        this.webSocket = new WebSocket(this.webSocketHost);
        this.webSocket.onopen = this.handleOnOpen;
        this.webSocket.onmessage = this.handleOnMessage;
        this.webSocket.onerror = this.handleOnError;
        this.webSocket.onclose = this.handleOnClose;
    },

    sendMessage: function(message){
        if (this.webSocket.readyState === WebSocket.OPEN){
            this.webSocket.send(JSON.stringify(message));
        }
    },

    handleOnOpen: function(){
        console.log("connection Open");
        document.title = "status: connected"
        Utility.drawFavicon(Colors.GREEN);
    },

    handleOnMessage: function(msg){
      console.log("Message received: "+msg.data);
    },

    handleOnClose: function(event){
        console.log("Connection closed. Code: " + event.code);
        document.title = "status: DISCONNECT"
        Utility.drawFavicon(Colors.RED);
    },

    handleOnError: function(error){
        console.log("WS: ERROR occured "+error);
    }
}
