$(function() {
  var jsonObj;
  var userID = '';
  $("#lock_ids").click(function(event) {
    /* Act on the event */
    console.log('set_up');
    userID = $('#userID').val()
  });
  

  function get_file() {
    data = $("#id_encrypted_file")[0].files[0]
    var reader = new FileReader()
    reader.readAsText(data)
    reader.onload = function(event) {
      jsonObj = JSON.parse(event.target.result);
    }
  }
  $("#load_file").click(function(event) {
    /* Act on the event */
    get_file()
    $("#response").html('File is loaded')
  });
  $('#register').click(function(event) {
    /* Act on the event */
    // event.preventDefault();
    // get_file()
    console.log($(this)[0].id);
    sendPost(jsonObj, $(this)[0].id)
  });

  $('#start_session').click(function(event) {
    // get_file()
    // event.preventDefault();
    console.log('click');
    sendPost(jsonObj, $(this)[0].id, start_session_template)
  });
  $("#users").click(function(event) {
    /* Act on the event */
    console.log('users');
    sendPost(jsonObj, $(this)[0].id + '/' + userID +'/', ussers_template)
  });
  $("#accounts").click(function(event) {
    /* Act on the event */
    console.log('accounts');
    sendPost(jsonObj, $(this)[0].id + '/' + userID +'/', ussers_template)

    
  });
  $("#payment").click(function(event) {
    /* Act on the event */
    console.log('payment');
  });
  $("#card").click(function(event) {
    /* Act on the event */
    console.log('card');
  });
  $("#mastercard_action").click(function(event) {
    /* Act on the event */
    console.log('mastercard_action');
  });
});

function sendPost(json, action, template) {
  $('#response').html('Loading...')
  csrftoken = Cookies.get('csrftoken')

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  frm = $("#encryption_form");
  $.ajax({
      url: '/API/' + action,
      type: frm.attr('method'),
      dataType: '',
      data: {
        'json': JSON.stringify(json),
        'pass': $('#id_encryption_password').val()
      },
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    })
    .done(function(response) {
      r = JSON.parse(response)
      // r = response
      console.log(r);
      // $("#response").html(response)
      if (r.Response) {
        show(r.Response, false, template)
      } else {
        show(r, true)
      }




    })
    .fail(function() {})
    .always(function() {});
}

function show(j, error, template) {
  // var template = $('#template').html()
  // // Mustache.parse(template)
  // var rendered;
  if (error) {
    $("#response").html(j.error_description_translated)

  } else {

    // rendered = Mustache.render(template, j)
    // $("#response").html(rendered)
    $.get(template, function(template){
      var rendered = Mustache.render(template, j)
      $('#response').html(rendered)
    })
  }
}
