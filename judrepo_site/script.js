let processosData = []; // Store all data for filtering

// Load CSV and initialize table
Papa.parse("processos.csv", {
  download: true,
  header: true,
  complete: function(results) {
    processosData = results.data;
    renderTable(processosData);
  }
});

// Render table rows
function renderTable(data) {
  const tbody = document.querySelector("#processos-table tbody");
  tbody.innerHTML = ""; // Clear existing rows

  data.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><a href="${row.Link}" target="_blank">${row.Link}</a></td>
      <td>${row.Data}</td>
      <td>${row.Comarca}</td>
      <td>${row.Vara}</td>
      <td>${row.Juiz}</td>
      <td>${row.Réu}</td>
      <td>${row.Tipo}</td>
    `;
    tbody.appendChild(tr);
  });
}

// Filter table by type
function filterTable(type) {
  const filteredData = type === "todos" 
    ? processosData 
    : processosData.filter(row => row.Tipo === type);
  renderTable(filteredData);
}
