function doRender(anid) {
    $.ajax({
        url: "/notation/" + pieceId + "/" + startMeas + "/" + endMeas,
        dataType: 'json',
        success: function(data, status, xhr) {
            console.log(data);
            modal = $("<div />", {
                "id": "myModal"
            }).appendTo("body");

            $("<div />", {
                "id": "myModalBody"
            }).appendTo(modal);

            $("#myModalBody").append(data['music']);

            var MEI = $('#meiScore');
            var cv = $('div#music canvas')[0];
            render_notation(MEI, cv, data['dimensions'][0], data['dimensions'][1]);
            $('#myModal').dialog({
                height: 500,
                width: 920,
                modal: true,
                title: "Example"
            });
        }
    });
}