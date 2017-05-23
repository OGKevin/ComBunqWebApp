var dataTable;

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
  $("#load_file").click(function(event) {
    get_file()
    deactivateItems()
    $(this).addClass('active')
    $("#loading").html('File is loaded... Starting session')
    setTimeout(function () {
      
      sendPost(jsonObj, "start_session", start_session_template)
    }, 500)

  });
  $('#register').click(function(event) {
    deactivateItems()
    $(this).addClass('active')
    sendPost(jsonObj, $(this)[0].id, register_template)
  });

  $('#start_session').click(function(event) {
    deactivateItems()
    $(this).addClass('active')
    sendPost(jsonObj, $(this)[0].id, start_session_template)
  });
  $("#users").click(function(event) {
    deactivateItems()
    $(this).addClass('active')
    sendPost(jsonObj, $(this)[0].id + '/' + get_user_id() + '/', ussers_template)
  });
  $("#accounts").click(function(event) {
    deactivateItems()
    $(this).addClass('active')
    sendPost(jsonObj, $(this)[0].id + '/' + get_user_id() + '/' + get_account_id(), accounts_template)


  });
  $("#payment").click(function(event) {
    deactivateItems()
    $(this).addClass('active')
    sendPost(jsonObj, $(this)[0].id + '/' + get_user_id() + '/' + get_account_id(), payments_template)

  });
  $("#card").click(function(event) {
    deactivateItems()
    $(this).addClass('active')
    sendPost(jsonObj, $(this)[0].id + '/' + get_user_id() + '/' + get_account_id(), card_template)

  });
  $("#mastercard_action").click(function(event) {});
  $("#export_transactions").click(function(event) {
    deactivateItems()
    $(this).addClass('active')
    pages = $("#pages").val()
    if (dataTable) {
      curentPage = dataTable.currentPage
      if (pages) {

        dataTable.export('csv', 'Bunq-transactions', ';', '\r\n', [pages])
      } else {
        dataTable.export('csv', 'Bunq-transactions', ';', '\r\n', curentPage)

      }
    } else {
      $("#loading").html('Table is not created yet?')
    }
  });
  $("#export_invoice").click(function(event) {
    deactivateItems()
    $(this).addClass('active')
    sendPost(jsonObj, 'invoice/' + get_user_id())
  });
});

function get_user_id() {
   return  $('#userID').val()
}
function get_account_id() {
  return  $("#accountID").val()
}

function sendPost(json, action, template) {
  $('#loading').html('<div class="ui segment"><div class="ui active inverted dimmer"><div class="ui large text loader">Loading</div></div>')
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
      if (r.Error !== undefined) {
        show(r.Error[0], true)
      } else if (r.Response[0].Payment) {
        createTable(r.Response)
      } else if (r.Response[0].status) {
        $("#response").html(r.Response[0].status)
        $.fileDownload('./invoice')
        .done(function () { alert('File download a success!'); })
        .fail(function () { alert('File download failed!'); });
      } else if (r.Response) {
        show(r.Response, false, template)
      }
    })
    .fail(function() {
      e = {
        'error_description_translated': 'Something went wrong server-side. Did you input you encrypted JSON file?'
      }
      show(e, true)
    })
    .always(function() {
      $("#loading").html('')
    });
}

function show(j, error, template) {
  if (error) {
    $("#response").html(j.error_description_translated)

  } else {
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
  if (dataTable) {
    dataTable.destroy();
  }
  dataTable = new DataTable("#response2", options);
}

function deactivateItems() {
  $("#load_file, #register, #start_session, #users, #accounts, #lock_ids, #payment, #card, #mastercard_action, #export_transactions, #export_invoice").removeClass('active')
}
