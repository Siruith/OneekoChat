$(document).ready(function () {
    var namespace = "/Neko";
    var socket = nya.connect("http://" + document.domain + ":" + location.port + namespace);

    socket.on("connected", function() {
        console.log("Connected");
    });

    socket.on("disconnected", function() {
        console.log("Disconnected");
    });

    socket.on("notification", function(message) {
        $("#chat-output").append(
            "<div>" + message + "</div>"
        );

        $("#chat-output").scrollTop($("#chat-output")[0].scrollHeight);
    });

    $("#clear-button").on("click", function () {
        $("#chat-input").val("");
    });

    $("#chat-form").on("submit", function () {
        socket.emit("notification", $("#chat-input").val());
        $("#chat-input").val("");
        return false;
    });

    $("#test-button").on("click", function () {
        var message = "Value " + Math.random();
        console.log("New message sent: ", message);
        socket.emit("notification", message);
    });
});