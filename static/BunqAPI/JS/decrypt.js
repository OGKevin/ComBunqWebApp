$(function(){
  $('#file_decrypt').click(function(event) {
    /* Act on the event */
    event.preventDefault();
    data = $('#id_encrypted_file')[0].files[0]
    var reader = new FileReader()
    reader.readAsText(data)
    reader.onload = function(event) {
    var jsonObj = JSON.parse(event.target.result);
    pass =  $('#id_encryption_password').val()
    
    sendPost(jsonObj)
  }
    });
  });

function sendPost(json) {
    csrftoken = Cookies.get('csrftoken')

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    frm = $("#encryption_form");
    $.ajax({
            url: frm.attr('action'),
            type: frm.attr('method'),
            dataType: '',
            data: {
                'json': JSON.stringify(json),
                'pass' : $('#id_encryption_password').val()
            },
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        })
        .done(function(response) {
            $("#response").html(response)
            
        })
        .fail(function() {})
        .always(function() {});
}
