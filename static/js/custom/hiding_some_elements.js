$(document).ready(function () {
    var url = document.referrer
    var splitted_url = url.split('/')
    var last_one = splitted_url.pop()
    var new_url = splitted_url.join('/')
    var path = new_url.split('/').pop()

    if (path === 'your_images'){
        document.getElementById("write_a_commment").style.display = "none";
        // document.getElementById("edit_button").style.display = "none";
    }
    else if(path === 'shared_images'){
        document.getElementById("share_button").style.display = "none";
    }

    }
);
