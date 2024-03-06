function makeChart(data) {
  console.log(data)

  var dates = data.map(function (d) {
    return d.Date;
  });
  var confirmedData = data.map(function (d) {
    return +d.Confirmed;
  });

  var chart = new Chart('chart', {
    type: "line",
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      scales: {
        y: {
          min: 0
        }
      },
    },
    data: {
      labels: dates,
      datasets: [
        {
          data: confirmedData
        }
      ]
    }
  });
}

Papa.parse("snapcraft-launchpad.csv", {
  download: true,
  dynamicTyping: true,
  header: true,
  complete: function (data) {
    makeChart(data.data)
  }
});


function snapcraftDeps(data) {
  console.log(data)
    // Get a reference to the div
    var myDiv = document.getElementById("snapcraft-deps");

    var libraries = data.map(function (d) {
      return d.library;
    });
    var versions = data.map(function (d) {
      return d.versions;
    });

    var parsed_data = []
    parsed_data.push(["library", "version"])
    for (var i = 0; i < data.length; i++) {
      var row = [];
      // Iterate over the keys (columns) of the object
      for (var key in data[i]) {
          if (data[i].hasOwnProperty(key)) {
              row.push(data[i][key]);
          }
      }
      // Push the constructed row to parsedData
      parsed_data.push(row);
  }


    var table = document.createElement('table');

    // Iterate through the parsed data
    parsed_data.forEach(function(rowData) {
        // Create a row for each row of data
        var row = document.createElement('tr');

        // Iterate through the row's data and create cells
        rowData.forEach(function(cellData) {
            var cell = document.createElement('td');
            cell.appendChild(document.createTextNode(cellData));
            row.appendChild(cell);
        });

        // Add the row to the table
        table.appendChild(row);
    });

    // Add the table to the container div
    myDiv.appendChild(table);

    // Check if the div exists
    //if (myDiv) {
    //    // Populate the div with content
    //    myDiv.innerHTML = libraries;
    //} else {
    //    console.error("Element with id 'snapcraft-deps' not found.");
    //}
}

Papa.parse("snapcraft-deps.csv", {
    download: true,
    dynamicTyping: true,
    header: true,
    complete: function (data) {
        snapcraftDeps(data.data)
    }
});
