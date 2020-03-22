d3.json("/world_data", function(error, data) {
    if (error) throw error;
    console.log(data)
      d3.select("tbody")
      .selectAll("tr")
      .data(data)
      .enter()
      .append("tr")
      .html(function(d) {
    return `<td>${d.Date}</td><td>${d.NewCases}</td><td>${d.NewDeaths}</td><td>${d.TotalDeaths}</td><td>${d.TotalCases}</td>`;
    });
});