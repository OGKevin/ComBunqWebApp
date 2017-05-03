$(function() {
  var jsonObj;
  function get_file() {
    data = $("#id_encrypted_file")[0].files[0]
    var reader = new FileReader()
    reader.readAsText(data)
    reader.onload = function(event) {
      jsonObj = JSON.parse(event.target.result);
    }
  }

  /*
  This is not working smooth, it seems that if you press the start_session button
  the POST request is being send twice (check js console).
  
  On the first click (both buttons combined), the file is not being read.
  Thie error will be raised:
      "Too many requests. You can do a maximum of 1 POST call per 1 second to this endpoint."
  On the seccond click it work as intended with the exception of the above issue.
  */
  $('#file_decrypt').click(function(event) {
    /* Act on the event */
    // event.preventDefault();
    console.log('click register');
    get_file()
    sendPost(jsonObj, 'register')
    
    $('#start_session').click(function(event) {
      console.log('click start sessoin');
      get_file()
      // event.preventDefault();
      sendPost(jsonObj, 'start_session')
      /* Act on the event */
    });
  });
});

function sendPost(json, action) {
  $('#response').html('Loading...')
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
      console.log(r);
      console.log(r.error);
      if (r.Error) {
        show(r.Error[0].error_description_translated, true);
      } else if (r.Response) {
        show(r.Response, false);
      } else if (r.error) {
        show(r.error, true)
      }




    })
    .fail(function() {})
    .always(function() {});
}

function show(j, error) {
  var template = $('#template').html()
  // Mustache.parse(template)
  var rendered;
  if (error) {
    $("#response").html(j)

  } else {
    console.log(j);
  
    rendered = Mustache.render(template, j)
    console.log('RENDERED', rendered)
    $("#response").html(rendered)
  }
}
