$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};
    websocketClient.init();
})

var websocketClient = {
    ws: null,

    init: function() {
        var url = "ws://" + location.host + "/websocket";
        this.ws = new WebSocket(url);
        this.ws.onopen = this.onopen;
        this.ws.onmessage = this.onmessage
        this.ws.onerror = this.onerror;
        this.ws.onclose = this.onclose;
    },

    send: function(message){
        if (this.ws){
            this.ws.send(message);
        }
    }, 

    onopen: function() {
        var message = websocketClient.formatMessage("onopen", "WebSocket onopen");
        // this.send(message);
        console.log(message)
    },

    onmessage: function(event) {
        var obj = JSON.parse(event.data);
        if ('data' in obj){
            var data = obj.data;
            $('.container').html(data);

            $('td>a').each(function(index){
                $(this).removeAttr("onclick");
                $(this).on("click", function(){
                    console.log(index)
                })
            })
        }
        console.log(obj);
    },

    onclose: function(event){
        console.log("WebSocketClose!", event);
    }, 

    onerror: function(event){
        console.log("WebSocketError!", event);
    },

    formatMessage: function(rpcName, rpcMessage){
        var rpc = {
            "rpcVersion": "1.0",
            "rpcName": rpcName,
            "rpcMessage": rpcMessage,
        };
        return JSON.stringify(rpc);
    }
};