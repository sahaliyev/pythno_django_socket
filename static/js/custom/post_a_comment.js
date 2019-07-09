$(document).ready(function () {
        $('#post_a_comment').submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: 'POST',
                url: '',
                data: {
                    comment: $('#comment').val(),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function () {
                    console.log('posted')
                }
            })
        });

    }
);
