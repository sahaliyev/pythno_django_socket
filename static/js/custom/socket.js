$(document).ready(function () {
    var session_user = document.getElementById("session_user").value;
    var formData = $('#post_comment');
    var comment = $('#comment');

    var starting = 'ws://';
    var protocol = window.location.protocol;
    if (protocol == 'https:') {
        starting = 'wss://';
    }

    var endpoint = starting + window.location.host + window.location.pathname;
    var socket = new ReconnectingWebSocket(endpoint);
    var chatHolder = $('#comment_holder');

    socket.onmessage = function (e) {
        console.log(e);
        var data = JSON.parse(e.data);

        // console.log(data);

        function append_data(pk, owner, comment) {
            if (owner === parseInt(session_user)) {
                var edit_button = $('<button>Edit</button>').attr({
                    "value": comment,
                    "data-id": pk,
                    'data-toggle': 'modal',
                    'id': 'edit_comment_' + pk,
                    'class': 'buttons edit_comment btn btn-primary',
                    'data-target': '#editModal',

                });
            }
            var delete_button = $('<button>Delete</button>').attr({
                "data-id": pk,
                'data-toggle': 'modal',
                'id': 'delete_comment',
                'class': 'delete_comment btn btn-danger',
                'data-target': '#deleteModal'
            });

            // console.log(pk);
            if ($("#comment_holder_" + pk).length > 0) {
                $("#comment_holder_" + pk).text(comment);
                $("#edit_comment_" + pk).val(comment);

            } else {
                var comment_holder = $("<h4>").text(comment).attr({
                    id: 'comment_holder_' + pk,
                    class: 'comment_holder'
                });

                chatHolder.append($("<div class='card'>").attr({id: 'comment_holder_card_' + pk})
                    .append($("<div class='card-body'>")
                        .append(comment_holder))
                    .append($("<div class='card-footer'>")
                        .append(edit_button)
                        .append(delete_button)))
            }

        }

        console.log(data.length)

        if (data.length > 0) {
            $('#comment_holder').empty();

            for (var i = 0; i < data.length; i++) {
                append_data(data[i].id, data[i].owner, data[i].comment)
            }

        } else if (data.length === undefined) {
            append_data(data.id, data.owner, data.comment)
        } else if (data.length === 0) {
            $('#comment_holder').empty();
        }
    };

    // EDITING COMMENT

    var comment_id = '';
    var comment_text = '';

    $(document).on('click', '.edit_comment', function () {
        comment_id = $(this).data('id');
        comment_text = $(this).val();

        $('#edited_comment_text').val(comment_text);
        $("#editModal").modal();
    });

    $('#edited_comment_text').change(function () {
        comment_text = $(this).val();
    });

    //DELETING COMMENT

    $(document).on('click', '.delete_comment', function () {
        comment_id = $(this).data('id');

    });


    socket.onopen = function (e) {
        console.log('open', e);
        formData.submit(function (event) {
            event.preventDefault();
            var com = comment.val();
            var finalData = {
                'type': 'new_comment',
                'message': com
            };
            socket.send(JSON.stringify(finalData));
            formData[0].reset()
        });

        //editing
        $('#edit_comment_form').submit(function (e) {
            e.preventDefault();
            var data = {
                'type': 'editing_comment',
                'comment_id': comment_id,
                'new_comment': comment_text
            };
            socket.send(JSON.stringify(data));
            $('#editModal').modal("hide");

        });

        //deleting
        $('#delete_comment_form').submit(function (e) {
            e.preventDefault();
            var data = {
                'type': 'deleting_comment',
                'comment_id': comment_id
            };
            socket.send(JSON.stringify(data));
            $('#deleteModal').modal("hide");
            // $('#comment_holder_card_' + comment_id).remove();
            // $('#comment_holder').empty();


        });

    };
    socket.onerror = function (e) {
        console.log('error', e)
    };

    socket.onclose = function (e) {
        console.log('close', e)
    };

})
;
