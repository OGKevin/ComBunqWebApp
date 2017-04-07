$(function() {
    // $("#textCSV").click(function(event) {
    //     complete = function(results, file) {
    //         getUserGraphs(results);
    //     };
    //     Configuration = {
    //         delimiter: "", // auto-detect
    //         newline: "", // auto-detect
    //         quoteChar: '"',
    //         header: true,
    //         dynamicTyping: true,
    //         preview: 0,
    //         encoding: "",
    //         worker: false,
    //         comments: true,
    //         step: undefined,
    //         complete: complete,
    //         error: undefined,
    //         download: false,
    //         skipEmptyLines: true,
    //         chunk: undefined,
    //         fastMode: undefined,
    //         beforeFirstChunk: undefined,
    //         withCredentials: undefined
    //     };
    //     Papa.parse($("#input").val(), Configuration);
    //
    //
    //
    //
    // });

    $("#textCSV").click(function(event) {
        // sendPost()
    
        input = $("#id_JSONTransactions").val()
        console.log('click');
        console.log(input);
        parseCSV(input)
    });
    $('#fileCSV').click(function(event) {
        file = $('#file')[0].files[0]
        complete = function(results, file) {
            getUserGraphs(results);
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
        Papa.parse(file, Configuration);


    })
});

function getGraphsDB(data) {
    income = [],
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
    var chart = AmCharts.makeChart("chartdiv2", {
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
        }
    });
}

function getUserGraphs(results) {
    income = []
    expenses = []
    for (var i = 0; i < results.data.length; i++) {
        number = Number(results.data[i].Bedrag.replace(",", '.'))
        name = results.data[i].Naam
        if (number < 0) {
            expenses.push({
                'name': name,
                'ammount': number * -1
            })
        } else {
            income.push({
                'name': name,
                'ammount': number
            })
        }

    }

    var chart = AmCharts.makeChart("chartdiv4", {
        "type": "pie",
        "theme": "light",
        "dataProvider": expenses,
        "valueField": "ammount",
        "titleField": "name",
        "colorField": "color",
        "balloon": {
            "fixedPosition": true
        }
    });
    var chart = AmCharts.makeChart("chartdiv3", {
        "type": "pie",
        "theme": "light",
        "dataProvider": income,
        "valueField": "ammount",
        "titleField": "name",
        "colorField": "color",
        "balloon": {
            "fixedPosition": true
        }
    });
}
function parseCSV(csv) {
  
  complete = function(results, file) {
    console.log('parse complete');
    console.log(results.data);
          sendPost(results);
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
frm.submit(function(event) {
  console.log('submiting before prevent ');
    event.preventDefault()
    console.log('submitting');
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
          console.log(response);
          console.log(typeof(response));
          console.log(JSON.parse(response));
          sortedJSON = JSON.parse(response);
          getUserGraphs2(sortedJSON);
          
        })
        .fail(function() {})
        .always(function() {
          console.log('send');
        });
});

}

function getUserGraphs2(data) {
    income = [],
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

    var chart = AmCharts.makeChart("chartdiv4", {
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
    var chart = AmCharts.makeChart("chartdiv3", {
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
        }
    });
}
