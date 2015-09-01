$(document).ready(function() {
    $("#gotodalpay").click(function() {
        console.log("hello");
        $("#dalpay").submit();
    });
    $("#btc").click(function() {
        $.get("/home/btcaddr", {}, function (json) {
            console.log(json['btc_addr'])
            $("#btcaddr").text(json['btc_addr'])
            var qrcode = $('<img/>', {'src': "/qrcode/" + json['btc_addr'],
                                      'align': 'middle',
                                      'width': '150px',
                                      'height': '150px'});
            $("#qrcode").html(qrcode);
        }, "json")
    });
});

