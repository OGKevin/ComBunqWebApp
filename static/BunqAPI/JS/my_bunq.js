var dataTable;

$(function() {
  var jsonObj;
  sendPost(jsonObj, "load_file", false)
  
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
    get_file()
    deactivateItems()
    $(this).addClass('active')


    setTimeout(function() {
      sendPost(jsonObj, "load_file", false)

    }, 500)
  });

  $("#load_file").click(function(event) {
    // firstCall()
    get_file()
    deactivateItems()
    $(this).addClass('active')


    setTimeout(function() {
      sendPost(jsonObj, "load_file", false)

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
      // getTableData()
      json = $("#transaction_table").tableToJSON()
      sendPost(json, 'filecreator/transactions/csv')
      // curentPage = dataTable.currentPage
      // if (pages) {
      //
      //   dataTable.export('csv', 'Bunq-transactions', ';', '\r\n', [pages])
      // } else {
      //   dataTable.export('csv', 'Bunq-transactions', ';', '\r\n', curentPage)
      //
      // }
    } else {
      $("#loading").html('Table is not created yet?')
    }
  });
  $("#export_invoice").click(function(event) {
    deactivateItems()
    $(this).addClass('active')
    sendPost(jsonObj, 'invoice/' + get_user_id())
  });

  $("#export_payment").click(function(event) {
    /* Act on the event */
    deactivateItems()
    $(this).addClass('active')
    sendPost(jsonObj, 'get_payment_pdf/' + get_user_id() + '/' + get_account_id() + '/' + get_payment_id())
  });
  $("#export_payment2").click(function(event) {
    /* Act on the event */
    deactivateItems()
    $(this).addClass('active')
    sendPost(jsonObj, 'customer_statement/' + get_user_id() + '/' + get_account_id() + '/' + get_format_type() + '/' + get_begin_date() + '/' + get_end_date() + '/' + 'european')
  });
});

function get_user_id() {
  return $('#userID').val()
}

function get_account_id() {
  return $("#accountID").val()
}

function get_payment_id() {
  return $('#paymentID').val()
}

function get_begin_date() {
  return $('#begin_date').val()
}

function get_end_date() {
  return $('#end_date').val()
}

function get_format_type() {
  return $("#format_type").val()
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

        } else if (action.match(/load_file/)) {
          show(r.start_session, false, start_session_template, 'start_session')
          show(r.accounts, false, accounts_template, 'accounts')
          createTable(r.payments, payments_template)


        } else if (action.match(/accounts/)) {
          show(r.Response, false, template, "accounts")
        } else if (action.match(/get_payment_pdf/)) {
          $.fileDownload('/filecreator/download')
            .done(function() {
              alert('File download a success!');
            })
            .fail(function() {
              alert('File download failed!');
            });
        } else if (action.match(/payment/)) {
          createTable(r.Response, template)
        } else if (action.match(/invoice/)) {
          $.fileDownload('/filecreator/download')
            .done(function() {
              alert('File download a success!');
            })
            .fail(function() {
              alert('File download failed!');
            });

        } else if (action.match(/filecreator/)) {
          $.fileDownload('/filecreator/download')
            .done(function() {
              alert('File download a success!');
            })
            .fail(function() {
              alert('File download failed!');
            });
        } else if (action.match(/customer_statement/)) {
          $.fileDownload('/filecreator/download')
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
        'error_description_translated': 'Something went wrong server-side. Not sure what exaclty :('
      }
      show(e, true)
    })
    .always(function() {
      $("#loading").html('')
    });
}

var payment_id;
$(document).delegate('.table-click', 'click', function(event) {
    /* Act on the event */
    // let Popup = new PopupClass({width: 200, maxHeight: 100}, false, false);
    payment_id = $(this).data("id")
    sendPost(null, 'payment' + '/' + get_user_id() + '/' + get_account_id() + '/' + payment_id, single_transaction_template)
    setTimeout(function(){
      
      $("#single_transaction").bPopup()
    }, 1000)
    // Popup.show(data)
    // console.log(data);
});

$(document).delegate('#export_payment2', 'click', function(event) {
  sendPost(null, 'get_payment_pdf/' + get_user_id() + '/' + get_account_id() + '/' + payment_id)
});

$(document).delegate('.search', 'keyup', function(event) {
  var $rows = $('#table-trans tbody tr');
      var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
      
      $rows.show().filter(function() {
          var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
          return !~text.indexOf(val);
      }).hide();
});

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

function createTable(input, template) {

  // var rows = [],
  //   headers = [
  //     'Payment ID',
  //     'Account ID',
  //     'Date',
  //     'Amount',
  //     // 'Account IBAN',
  //     'Payee IBAN',
  //     'Name',
  //     'Description',
  //     // 'Type'
  //   ]
  console.log(input);
  numeral.locale("nl-nl")
  for (var i = 0; i < input.length; i++) {
    // rows.push([
      // input[i].Payment.id,
      // input[i].Payment.monetary_account_id,
      input[i].Payment.updated = moment(input[i].Payment.updated.slice(0, 10)).format("MMM Do YYYY"),
      input[i].Payment.amount.value = numeral(input[i].Payment.amount.value.replace(".", ",")).format('$0,0[.]00')
      // input[i].Payment.alias.iban,
      // input[i].Payment.counterparty_alias.iban,
      // input[i].Payment.counterparty_alias.label_user.public_nick_name,
      // input[i].Payment.description,
      // input[i].Payment.type
    // ])
  }
  // options = {
  //   data: {
  //     'headings': headers,
  //     "rows": rows
  //   }
  // }
  // if (dataTable) {
  //   dataTable.destroy();
  // }
  // dataTable = new DataTable("#transaction_table", options);
  // $("#transaction_table").css('visibility', 'visible');
  // $("#user_payments").css('visibility', 'visible');
  data = {
    // 'headers': headers,
    'rows': input
  }
  arr = template.split("/")
  $.get(template, function(template) {
    rendered = Mustache.render(template, data)
    if (arr[arr.length-1] == "payments.html"){
      $("#transaction_table").html(rendered)
      $("#user_payments").css('visibility', 'visible');
      
    }else{
      $("#single_transaction").html(rendered)
    }
    // console.log(rendered);
    
  })
}

function deactivateItems() {
  $("#load_file, #register, #start_session, #users, #accounts, #lock_ids, #payment, #card, #mastercard_action, #export_transactions, #export_invoice").removeClass('active')
}

function getTableData() {
  table = dataTable
  json = $("#transaction_table").tableToJSON()
  // for (var i = 0; i < table.rows.length; i++) {
  //   data.push(table.rows[i].innerHTML)
  // }
}
