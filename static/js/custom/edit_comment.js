$(document).ready(function () {
        var comment_id = '';
        var comment_text = '';

        $(document).on('click', '.buttons', function () {
            comment_id = $(this).data('id');
            comment_text = $(this).val();
            console.log(comment_id, comment_text)
            $('#editModal').modal("show");

            $('#edited_comment_text').val(comment_text);
            $("#editModal").modal();
        });

        $('#edited_comment_text').change(function () {
            comment_text = $(this).val();
        });


        $('#edit_comment_form').submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: 'POST',
                url: '/edit_comment/',
                data: {
                    comment_id: comment_id,
                    comment_text: comment_text,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function (data) {
                    $('#editModal').modal("hide");
                    alert(data.message);
                },
                error: function (data) {
                    alert(data.message);
                }
            })
        });
    }
);
