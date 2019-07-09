$(document).ready(function () {
        var comment_id = ''
        $(".delete_comment").click(function () {
            comment_id = $(this).data('id');
            console.log('efhbas')

            // $("#deleteModal #exampleModalLabel ").append(comment_id);
        });

        $('#delete_comment_form').submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: 'POST',
                url: '/delete_comment/',
                data: {
                    comment_id: comment_id,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function (data) {
                    $('#deleteModal').modal("hide");
                    alert(data.message);
                },
                error: function (data) {
                    alert(data.message);
                }
            })
        });
    }
);
