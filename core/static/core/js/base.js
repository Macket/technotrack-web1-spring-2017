$(document).ready(function () {

    function autoload() {

        $('.autoload').each(function () {
        $(this).load($(this).data('url'));
    });

    }

    window.setInterval(autoload, 2000)


    $('.dialog-link').click( function () {
        $('#exampleModal').modal();
        $('.modal-body').load($(this).attr('href'));
        return false
    });

    $(document).on('submit', '.ajax-form', function () {
        var form = $(this);
        $.post(form.attr('action'), form.serialize(), function (data) {
            if (data == 'OK') {
                location.reload();
            }
            form.html(data)
        });
        return false;
    });

    function updateLikes() {

        $('.like').each( function () {
            $(this).load($(this).data('url'));
        });
    }

    window.setInterval(updateLikes, 1000)


    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $('meta[name=csrf]').attr("content"));
            }
        }
    });

     $(document).on('click', 'button.ajaxlike', function() {
         var url = $(this).data('url');
         var postid = $(this).data('postid');
         var element = $(this);
         $.post(url, function (data) {
             $('#likes-'+ postid).html(data)
         });
     });
});