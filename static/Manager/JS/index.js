$(function() {
    $("#textCSV").click(function(event) {
        // sendPost()

        input = $("#id_JSONTransactions").val()
        parseCSV(input)
    });

    $('#fileCSV').click(function(event) {
        // event.preventDefault()

        /* Act on the event */
        input = $('#id_JSONTransactionsFile')[0].files[0]
        parseCSV(input)
    });
});

function parseCSV(csv) {

    complete = function(results, file) {
        sendPost(results);
        // createTable(results);
        // NOTE: need a delay so that the pies load before the table shows
    };
    Configuration = {
        delimiter: "", // auto-detect
        newline: "", // auto-detect
        quoteChar: '"',
        header: true,
        dynamicTyping: true,
        preview: 0,
        encoding: "",
        worker: false,
        comments: true,
        step: undefined,
        complete: complete,
        error: undefined,
        download: false,
        skipEmptyLines: true,
        chunk: undefined,
        fastMode: undefined,
        beforeFirstChunk: undefined,
        withCredentials: undefined
    };
    Papa.parse(csv, Configuration);
}

function sendPost(json) {
    csrftoken = Cookies.get('csrftoken')

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    frm = $("#textCSVForm");
    $.ajax({
            url: frm.attr('action'),
            type: frm.attr('method'),
            dataType: '',
            data: {
                'json': JSON.stringify(json.data)
            },
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        })
        .done(function(response) {
            sortedJSON = JSON.parse(response);
            
            getUserGraphs(sortedJSON.catagories);
            createTable(sortedJSON.transactions);
        })
        .fail(function() {})
        .always(function() {});
}

function getUserGraphs(data) {
    var income = [],
        expenses = [];
    for (var i = 0; i < data.length; i++) {
        if (data[i][1] > 0) {
            income.push({
                'catName': data[i][0],
                'ammount': data[i][1]
            })

        } else {
            expenses.push({
                'catName': data[i][0],
                'ammount': data[i][1] * -1
            })

        }
    }

    var chart = AmCharts.makeChart("chartdiv", {
        "type": "pie",
        "theme": "light",
        "dataProvider": income,
        "valueField": "ammount",
        "titleField": "catName",
        "balloon": {
            "fixedPosition": true
        },
        "export": {
            "enabled": false
        }
    });
    var chart2 = AmCharts.makeChart("chartdiv2", {
        "type": "pie",
        "theme": "light",
        "dataProvider": expenses,
        "valueField": "ammount",
        "titleField": "catName",
        "balloon": {
            "fixedPosition": true
        },
          "export": {
            "enabled": false
        },
    });
}

function createTable(input) {
    var rows = [],
     headers = Object.keys(input[0]);
    for (var i = 0; i < input.length; i++) {
      rows.push(Object.keys(input[i]).map(function (key) { return input[i][key]; }))
      // NOTE: code climate doesnt want function inside loops
    }
    options = {
        data: {
            'headings':headers,
            "rows": rows
        }
    }
    var dataTable = new DataTable("#transactionsInfo", options)
}
