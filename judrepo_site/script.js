// Function to load and filter data
function loadFilteredData(tipo) {
  fetch("processos.json")
    .then(response => response.json())
    .then(data => {
      // Filter the data by 'Tipo'
      const filteredData = data.filter(row => row.Tipo === tipo);

      // Render the filtered data
      renderTable(filteredData);
    })
    .catch(error => console.error("Erro ao carregar os dados:", error));
}

// Function to render the table
function renderTable(data) {
  const tbody = document.getElementById("processos-tbody");
  const loadingMessage = document.getElementById("loading-message");

  // Show "Carregando..."
  loadingMessage.style.display = "block";
  tbody.innerHTML = ""; // Clear the table for fresh content

  // Simulate a delay for loading (optional, for testing)
  setTimeout(() => {
    // Build the rows as a single HTML string
    let rowsHTML = data.map(row => `
      <tr>
        <td><a href="${row.Link}" target="_blank">${row.Link.split("/").pop()}</a></td>
        <td>${row.Data}</td>
        <td>${row.Comarca}</td>
        <td>${row.Vara}</td>
        <td>${row.Juiz}</td>
        <td>${row.Réu}</td>
        <td>${row.Tipo}</td>
      </tr>
    `).join("");

    // Update the table content and hide the loading message
    tbody.innerHTML = rowsHTML;
    loadingMessage.style.display = "none";
  }, 100); // Optional delay
}

