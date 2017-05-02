$(function() {
  var jsonObj;
  $("#id_encrypted_file").change(function(event) {
    /* Act on the event */
    data = $(this)[0].files[0]
    var reader = new FileReader()
    reader.readAsText(data)
    reader.onload = function(event) {
      jsonObj = JSON.parse(event.target.result);
    }
  });
  $('#file_decrypt').click(function(event) {
    /* Act on the event */
    event.preventDefault();
    sendPost(jsonObj, 'register')
    $('#start_session').click(function(event) {
      console.log('click');
      event.preventDefault();
      sendPost(jsonObj, 'start_session')
      /* Act on the event */
    });
  });
});

function sendPost(json, action) {
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
        'pass': $('#id_encryption_password').val(),
        'action': action
      },
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    })
    .done(function(response) {
      r = JSON.parse(response)
      // $("#response").html(response)
      if (r.Error) {
        show(r.Error[0].error_description_translated, true);
      } else if (r.Response) {
        show(r.Response);
      }




    })
    .fail(function() {})
    .always(function() {});
}

function show(j, error) {
  if (error) {
    $("#response").html(j)

  } else {
    console.log(j);
    token = j[1].Token.token
    $("#response").html(token)
  }
}
