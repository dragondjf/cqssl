$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};
    websocketClient.init();
})


function notifyMe(html) {
  // Let's check if the browser supports notifications
  if (!("Notification" in window)) {
    alert(html);
  }

  // Let's check if the user is okay to get some notification
  else if (Notification.permission === "granted") {
    // If it's okay let's create a notification
    var notification = new Notification(html);
  }

  // Otherwise, we need to ask the user for permission
  else if (Notification.permission !== 'denied') {
    Notification.requestPermission(function (permission) {
      // If the user is okay, let's create a notification
      if (permission === "granted") {
        var notification = new Notification(html);
      }
    });
  }

  // At last, if the user already denied any notification, and you 
  // want to be respectful there is no need to bother them any more.
}


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
            var result = obj.result;
            console.log(result)
            $('#large').text(result.large);
            $('#small').text(result.small);
            $('#even').text(result.even);
            $('#odd').text(result.odd);
            $('.container>.row>.span8').html(data);
            $('td>a').each(function(index){
                $(this).removeAttr("onclick");
                $(this).on("click", function(){
                    console.log(index)
                })
            })

            // notifyMe($('.span4').html());
        }
        // console.log(obj);
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