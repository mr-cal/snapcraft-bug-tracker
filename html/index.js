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
    var div = document.getElementById("app-deps");
    var table = document.createElement('table');
    var header_row = true;

    // Iterate through the parsed data
    data.forEach(function(rowData) {
      // Create a row for each row of data
      if (rowData[0] === null) {
        return; // Skips the current iteration
      }
      var row = document.createElement('tr');
      console.log(rowData)

      // Iterate through the row's data and create cells
      rowData.forEach(function(cellData) {
        if (header_row) {
          var cell = document.createElement('th');
        } else {
          var cell = document.createElement('td');
        }
        cell.appendChild(document.createTextNode(cellData));
        row.appendChild(cell);

      });
      header_row = false;

      // Add the row to the table
      table.appendChild(row);
    });

    div.appendChild(table);
}

Papa.parse("app-deps.csv", {
    download: true,
    dynamicTyping: true,
    header: false,
    complete: function (data) {
        snapcraftDeps(data.data)
    }
});
