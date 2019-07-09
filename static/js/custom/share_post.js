$(document).ready(function () {
        var post_id = '';
        $(".share_post").click(function () {
            post_id = $(this).val();
            console.log(post_id)

        });

        var value = 0;
        $("#permission").change(function () {
            if ($(this).is(":checked")) {
                value = 1
            } else if ($(this).not(":checked")) {
                value = 0
            }
        });

        $('#share_post_form').submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: 'POST',
                url: '',
                data: {
                    post_id: post_id,
                    username: $('#username').val(),
                    permission: value,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function (data) {
                    $('#shareModal').modal("hide");
                    alert(data.message);
                },
                error: function (data) {
                    alert(data.message);
                    console.log(data)
                }
            })
        });

    }
);
