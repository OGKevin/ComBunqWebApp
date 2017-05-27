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
  $("#encryption_form").submit(function(event) {
    /* Act on the event */
    event.preventDefault()
    firstCall()
  });
  $("#load_file").click(function(event) {
    firstCall()
    deactivateItems()
    $(this).addClass('active')

  });

  function firstCall() {
    $("#user_accounts").css('visibility', 'hidden');
    get_file()
    setTimeout(function() {

      if (jsonObj) {
        
        $("#loading").html('File is loaded... Starting session')

          sendPost(jsonObj, "start_session", start_session_template)

        setTimeout(function() {
          sendPost(jsonObj, "accounts" + '/' + get_user_id(), accounts_template)

        }, 3000)

        setTimeout(function() {
          sendPost(jsonObj, "payment" + '/' + get_user_id() + '/' + get_account_id(), payments_template)

        }, 5000)
      } else {
        alert('You must load a file fist')
      }
    }, 500)

  }



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
  return $('#userID').val()
}

function get_account_id() {
  return $("#accountID").val()
}

function sendPost(json, action, template) {
  $('#loading').html('<div class="ui segment"><div class="ui active inverted dimmer"><div class="ui large text loader"></div></div>')
  csrftoken = Cookies.get('csrftoken')

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  frm = $("#encryption_form");
  $.ajax({
      url: '/API/' + action,
      type: 'POST',
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
      if (r.Error === undefined) {

        if (action.match(/start_session/)) {
          show(r.Response, false, template, "start_session")

        } else if (action.match(/accounts/)) {
          show(r.Response, false, template, "accounts")
        } else if (action.match(/payment/)) {
          createTable(r.Response)
        } else if (action.match(/invoice/)) {
          $.fileDownload('./download/invoice')
            .done(function() {
              alert('File download a success!');
            })
            .fail(function() {
              alert('File download failed!');
            });

        } else if (action.match(/users/)) {
          show(r.Response, false, template, "users")
        } else if (action.match(/card/)) {
          show(r.Response, false, template, "card")
        } else {
          error = {
            "error_description_translated": "Not sure what to do with this response, it might be empty ?"
          }
          show(error, true)
        }
      } else {
        show(r.Error[0], true)
      }

    })
    .fail(function() {
      e = {
        'error_description_translated': 'Something went wrong server-side. Not usre what exaclty :('
      }
      show(e, true)
    })
    .always(function() {
      $("#loading").html('')
    });
}

function show(j, error, template, location) {
  if (error) {
    $("#user_accounts").html(j.error_description_translated)
    $("#user_accounts").css('visibility', 'visible');


  } else {

    $.get(template, function(template) {
      rendered = Mustache.render(template, j)

      switch (location) {
        case "start_session":
          $("#user_profile").html(rendered)
          try {
            $("#userID").val(j[2].UserCompany.id)

          } catch (e) {
            $("#userID").val(j[2].UserPerson.id)

          } finally {
            $("#side_bar").css('visibility', 'visible');

          }
          break;
        case "accounts":
          $("#user_accounts").html(rendered)
          $("#user_accounts").css('visibility', 'visible');
          $("#accountID").val(j[0].MonetaryAccountBank.id)
          break;
        case "users":
          $("#user_accounts").html(rendered)
          break;
        case "card":
          $("#user_accounts").html(rendered)
        default:

      }
      // $("#" + location).html(rendered)
      // locatoin(rendered)
    })

  }
}

function createTable(input) {

  var rows = [],
    headers = [
      'Payment ID',
      'Account ID',
      'Date',
      'Amount',
      // 'Account IBAN',
      'Payee IBAN',
      'Name',
      'Description',
      // 'Type'
    ]
  numeral.locale("nl-nl")
  for (var i = 0; i < input.length; i++) {
    rows.push([
      input[i].Payment.id,
      input[i].Payment.monetary_account_id,
      moment(input[i].Payment.updated.slice(0, 10)).format("MMM Do YYYY"),
      numeral(input[i].Payment.amount.value.replace(".", ",")).format('$0,0[.]00'),
      // input[i].Payment.alias.iban,
      input[i].Payment.counterparty_alias.iban,
      input[i].Payment.counterparty_alias.label_user.public_nick_name,
      input[i].Payment.description,
      // input[i].Payment.type
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
  dataTable = new DataTable("#transaction_table", options);
  $("#transaction_table").css('visibility', 'visible');
}

function deactivateItems() {
  $("#load_file, #register, #start_session, #users, #accounts, #lock_ids, #payment, #card, #mastercard_action, #export_transactions, #export_invoice").removeClass('active')
}
