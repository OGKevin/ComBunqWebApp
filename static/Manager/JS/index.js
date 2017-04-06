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
$(function() {
    $("#textCSV").click(function(event) {
        complete = function(results, file) {
            console.log("Parsing complete", results);
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
        Papa.parse($("#input").val(), Configuration);

    });
  $('#fileCSV').click(function(event) {
    file = $('#file')[0].files[0]
    console.log(file);
    complete = function(results, file) {
        console.log("Parsing complete", results);
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
    Papa.parse(file , Configuration);


  });
})

function getUserGraphs(results) {
    income = []
    expenses = []
    console.log(typeof(Number(results.data[0].Bedrag)));
    for (var i = 0; i < results.data.length; i++) {
        number = Number(results.data[i].Bedrag.replace(",", '.'))
        name = results.data[i].Naam
        // console.log('DATA[I]', results.data[i])
        // console.log(results.data[i].Bedrag);
        if (number < 0) {
            console.log('expanse', number * -1, name);
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
    console.log('EXPENSES', expenses)

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
// getGraphs();
