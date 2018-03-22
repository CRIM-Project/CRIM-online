function editNoteAction() {
    $('.open-EditNote').on({
        'click': function(event) {
            var pieceid = $(this).data('pieceid');

            $.ajax({
                type: "GET",
                url: "/note/" + pieceid,
                dataType: 'json',
                success: function (json) {
                    showModalAction(pieceid, json);
                },
                error: function () {
                    showModalAction(pieceid);
                }
            });

            return false;
        }
    });
}

function deleteNoteAction() {
    $( ".open-DeleteNote" ).on({
        'click': function(event) {
            // The second parameter says NOT to return to editing the note
            confirmDeleteNoteAction($(this).data('pieceid'), false);
        }
    });
}

function showModalAction(pieceid, json) {
    // Remove old modal, if any
    $("#editNote").remove();

    // Title string
    var titletext = ('Edit Note to Piece ' + pieceid);
    var notetext = '';

    // Get CURRENT text of note -- not necessarily what
    // it was when template was loaded
    if (json) {
        notetext = json.text;
    }

    // Outer div for modal.
    var modal = $("<div />", {
        "id": "editNote",
        "class": "modal fade",
        "tabindex": "-1",
        "role": "dialog",
        "aria-labelledby": "editNote",
        "aria-hidden": "true",
    }).appendTo("body");

    // First layer div
    var modal_dialog = $("<div />", {
        "class": "modal-dialog",
    }).appendTo(modal);

    // Second layer div
    var modal_content = $("<div />", {
        "class": "modal-content",
    }).appendTo(modal_dialog);

    // Modal header div
    var modal_header = $("<div />", {
        "class": "modal-header",
    }).appendTo(modal_content);

    // Modal header: button
    var modal_header_button = $("<button />", {
        "type": "button",
        "class": "close",
        "data-dismiss": "modal",
        "aria-hidden": "true",
        "text": "×",
    }).appendTo(modal_header);

    // Modal header: text
    var modal_header_text = $("<h3 />", {
        "class": "modal-title",
        "id": "editNoteLabel",
        "text": titletext,
    }).appendTo(modal_header);

    // Modal body div
    var modal_body = $("<div />", {
        "class": "modal-body",
    }).appendTo(modal_content);

    // Modal body: paragraph
    var modal_body_p = $("<p />", {
        "id": "modal-body-p",
    }).appendTo(modal_body);

    // Modal body: form's piece ID
    var modal_body_pieceid = $("<input />", {
        "form": "modal-form",
        "type": "hidden",
        "name": "piece_id",
        "id": "piece-id",
        "value": pieceid,
    }).appendTo(modal_body_p);

    // Modal body: form's textarea
    var modal_body_textarea = $("<textarea />", {
        "form": "modal-form",
        "name": "text",
        "rows": "10",
        "id": "note-textarea",
        "style": "width:100%; -webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box;",
        "text": notetext,
    }).appendTo(modal_body_p);

    // Modal footer div
    var modal_footer = $("<div />", {
        "class": "modal-footer",
    }).appendTo(modal_content);

    // Only show button to delete if there was a note there in the first place
    if (notetext != '') {
        var modal_footer_delete = $("<button />", {
            "type": "button",
            "id": "modal-delete",
            "class": "btn btn-danger pull-left",
            "data-dismiss": "modal",
            "text": "Delete",
        }).appendTo(modal_footer);
    }

    // Modal footer: close
    var modal_footer_close = $("<button />", {
        "type": "button",
        "class": "btn",
        "data-dismiss": "modal",
        "text": "Close",
    }).appendTo(modal_footer);

    // Modal footer: save
    var modal_footer_save = $("<button />", {
        "form": "modal-form",
        "type": "submit",
        "id": "modal-save",
        "class": "btn btn-primary",
        "data-dismiss": "modal",
        "text": "Save changes",
    }).appendTo(modal_footer);

    $("#editNote").modal({
        "backdrop": "static",
    });

    $( "#modal-save" ).on({
        'click': function(event) {
            $('#modal-form').submit();
            event.preventDefault();
        }
    });

    $( "#modal-delete" ).on({
        'click': function(event) {
            // The second parameter says to return to editing the note
            confirmDeleteNoteAction(pieceid, true);
        }
    });
}

function submitNoteAction() {
    $( "#modal-form" ).submit(function( event ){
        var form = $(this);
        var serialized_data = form.serialize();
        var pieceid = document.getElementById("piece-id").value;
        $.ajax({
            type: "POST",
            url: "/notes/",
            data: serialized_data,
        });

        // If it was an Add Note button, make it now an Edit Note button
        // by removing "primary" class and changing text
        var button_fav = document.getElementById("button-fav-" + pieceid);
        if (button_fav) {
            button_fav.className = "btn btn-info open-EditNote";
            button_fav.innerHTML = "Edit Note";
            button_fav.title = "Edit Note to " + pieceid;
        }

        // Add the Delete Note button if it was missing
        var button_del = document.getElementById("button-del-" + pieceid);
        if (button_del) {
            button_del.className = "btn btn-danger open-DeleteNote";
            button_del.innerHTML = "Delete&nbsp;Note";
        }
        event.preventDefault();
    });
}

function confirmDeleteNoteAction(pieceid, returntomodal) {
    // Remove old modal, if any
    $("#confirmDelete").remove();

    // Title string
    var titletext = ('Delete Note to Piece ' + pieceid);

    // Outer div for modal.
    var modal = $("<div />", {
        "id": "confirmDelete",
        "class": "modal fade",
        "tabindex": "-1",
        "role": "dialog",
        "aria-labelledby": "confirmDelete",
        "aria-hidden": "true",
    }).appendTo("body");

    // First layer div
    var modal_dialog = $("<div />", {
        "class": "modal-dialog",
    }).appendTo(modal);

    // Second layer div
    var modal_content = $("<div />", {
        "class": "modal-content",
    }).appendTo(modal_dialog);

    // Modal header div
    var modal_header = $("<div />", {
        "class": "modal-header",
    }).appendTo(modal_content);

    // Modal header: button
    var modal_header_button = $("<button />", {
        "type": "button",
        "class": "close",
        "data-dismiss": "modal",
        "aria-hidden": "true",
        "text": "×",
    }).appendTo(modal_header);

    // Modal header: text
    var modal_header_text = $("<h3 />", {
        "class": "modal-title",
        "id": "confirmDeleteLabel",
        "text": titletext,
    }).appendTo(modal_header);

    // Modal body div
    var modal_body = $("<div />", {
        "class": "modal-body",
    }).appendTo(modal_content);

    // Modal body: paragraph
    var modal_body_p = $("<p />", {
        "id": "modal-body-p",
        "text": "Are you sure you want to delete this note?",
    }).appendTo(modal_body);

    // Modal body: form's piece ID
    var modal_body_pieceid = $("<input />", {
        "form": "modal-form",
        "type": "hidden",
        "name": "piece_id",
        "id": "piece-id",
        "value": pieceid,
    }).appendTo(modal_body_p);

    // Modal body: new text of the note, which is empty,
    // because we're deleting it
    var modal_body_textarea = $("<input />", {
        "form": "modal-form",
        "type": "hidden",
        "name": "text",
        "id": "text",
        "value": '',
    }).appendTo(modal_body_p);

    // Modal footer div
    var modal_footer = $("<div />", {
        "class": "modal-footer",
    }).appendTo(modal_content);

    var modal_footer_cancel = $("<button />", {
        "type": "button",
        "id": "cancel-delete",
        "class": "btn",
        "data-dismiss": "modal",
        "data-pieceid": pieceid,
        "text": "Cancel",
    }).appendTo(modal_footer);

    var modal_footer_delete = $("<button />", {
        "form": "modal-form",
        "type": "submit",
        "id": "confirm-delete",
        "class": "btn btn-danger",
        "data-dismiss": "modal",
        "text": "Delete",
    }).appendTo(modal_footer);

    $("#confirmDelete").modal({
        "backdrop": "static",
    });

    $( "#cancel-delete" ).on({
        'click': function(event) {
            if (returntomodal) {
                $.ajax({
                    type: "GET",
                    url: "/note/" + pieceid,
                    dataType: 'json',
                    success: function (json) {
                        showModalAction(pieceid, json);
                    },
                });
            }
        }
    });

    $( "#confirm-delete" ).on({
        'click': function(event) {
            $('#modal-form').submit();

            // If it was an Edit Note button, make it now an Add Note button
            // by adding "primary" class and changing text
            var button_fav = document.getElementById("button-fav-" + pieceid);
            if (button_fav) {
                button_fav.className = "btn btn-primary open-EditNote";
                button_fav.innerHTML = "Add Note";
                button_fav.title = "Add Note to " + pieceid;
            }

            // And do the same if it was in the "Pieces with notes" list
            var button_note = document.getElementById("button-note-" + pieceid);
            if (button_note) {
                button_note.className = "btn btn-primary open-EditNote";
                button_note.innerHTML = "Add Note";
                button_note.title = "Add Note to " + pieceid;
            }

            // Remove the old delete button
            var button_del = document.getElementById("button-del-" + pieceid);
            if (button_del) {
                button_del.className = "";
                button_del.innerHTML = "";
            }

            event.preventDefault();
        }
    });
}
