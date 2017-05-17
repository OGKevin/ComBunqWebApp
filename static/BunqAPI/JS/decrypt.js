
var dataTable;

$(function() {
  var jsonObj,
    userID = '',
    accountID = '';
  $("#lock_ids").click(function(event) {
    /* Act on the event */
    userID = $('#userID').val()
    accountID = $("#accountID").val()
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
    $("#loading").html('File is loaded')
  });
  $('#register').click(function(event) {
    /* Act on the event */
    // event.preventDefault();
    // get_file()
    sendPost(jsonObj, $(this)[0].id, register_template)
  });

  $('#start_session').click(function(event) {
    // get_file()
    // event.preventDefault();
    sendPost(jsonObj, $(this)[0].id, start_session_template)
  });
  $("#users").click(function(event) {
    /* Act on the event */
    sendPost(jsonObj, $(this)[0].id + '/' + userID + '/', ussers_template)
  });
  $("#accounts").click(function(event) {
    /* Act on the event */
    sendPost(jsonObj, $(this)[0].id + '/' + userID + '/' + accountID, accounts_template)


  });
  $("#payment").click(function(event) {
    /* Act on the event */
    sendPost(jsonObj, $(this)[0].id + '/' + userID + '/' + accountID, payments_template)
    
  });
  $("#card").click(function(event) {
    /* Act on the event */
    sendPost(jsonObj, $(this)[0].id + '/' + userID + '/' + accountID, card_template)
    
  });
  $("#mastercard_action").click(function(event) {
    /* Act on the event */
  });
  $("#export").click(function(event) {
    /* Act on the event */
    pages = $("#pages").val()
    if (dataTable) {
      curentPage = dataTable.currentPage
      if (pages) {
        
        dataTable.export('csv', 'Bunq-transactions', ';', '\r\n', [pages])
      }else {
        dataTable.export('csv', 'Bunq-transactions', ';', '\r\n', curentPage)
        
      }
    }else {
      $("#loading").html('Table is not created yet?')
    }
  });
});

function sendPost(json, action, template) {
  $('#loading').html('<i class="fa-5x fa fa-spinner fa-spin" aria-hidden="true"></i>')
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
      // $("#response").html(response)
      if (r.Error !== undefined) {
             show(r.Error[0], true)
              $("#loading").html('')
            }else if (r.Response[0].Payment) {
              createTable(r.Response)
              $("#loading").html('')
            } else if (r.Response){
              show(r.Response, false, template)
              $("#loading").html('')
            }
      
      //
      // else {
      //   show(r, true)
      // }

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
    $.get(template, function(template) {
      var rendered = Mustache.render(template, j)
      $('#response').html(rendered)
    })
  }
}



function createTable(input) {
  
    var rows = [],
        headers = [
          'Payment ID',
          'Account ID',
          'Date',
          'Ammount',
          'Account IBAN',
          'Payee IBAN',
          'Name',
          'Description',
          'Type'
        ]

    for (var i = 0; i < input.length; i++) {
        rows.push([
          input[i].Payment.id,
          input[i].Payment.monetary_account_id,
          input[i].Payment.updated,
          input[i].Payment.amount.value,
          input[i].Payment.alias.iban,
          input[i].Payment.counterparty_alias.iban,
          input[i].Payment.counterparty_alias.label_user.public_nick_name,
          input[i].Payment.description,
          input[i].Payment.type
        ])
    }
    options = {
        data: {
            'headings': headers,
            "rows": rows
        }
    }

    // Check to see if initialized
    if (dataTable) {
        // Wipe the table
        dataTable.destroy();

        // Destroy the containers
        // dataTable.wrapper.parentNode.replaceChild(dataTable.table, dataTable.wrapper);
        // dataTable.init(options)
    }

    // Initialize with the data
    dataTable = new DataTable("#response2", options);
    // dataTable.destroy()
}

function exportTable(){
  
}
