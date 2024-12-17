let processosData = []; // Armazena os dados carregados do JSON

// Carrega o JSON
fetch("processos.json")
  .then(response => response.json())
  .then(data => {
    processosData = data;
    renderTable(processosData); // Renderiza todos os dados inicialmente
  })
  .catch(error => console.error("Erro ao carregar JSON:", error));

// Função para renderizar a tabela
function renderTable(data) {
    const tbody = document.getElementById("processos-tbody");
    const start = performance.now();
    // Use a string to accumulate the table rows
    let rowsHTML = data.map(row => `
        <tr>
            <td><a href="${row.Link}" target="_blank">${row.Link}</a></td>
            <td>${row.Data}</td>
            <td>${row.Comarca}</td>
            <td>${row.Vara}</td>
            <td>${row.Juiz}</td>
            <td>${row.Réu}</td>
            <td>${row.Tipo}</td>
        </tr>
    `).join("");
    const end = performance.now();
    console.log(`Tempo para loop: ${end - start} ms`);

    // Update the DOM once
    tbody.innerHTML = rowsHTML;
    const end2 = performance.now();
    console.log(`Tempo para renderizar: ${end2 - end} ms`);
}
  

// Função para filtrar a tabela
function filterTable(tipo) {
    // Medir tempo para filtrar
    const start = performance.now();

    if (tipo === "todos") {
        renderTable(processosData);
    } else {
        const filteredData = processosData.filter(row => row.Tipo === tipo);
        renderTable(filteredData);
    }

    // Medir tempo para filtrar
    const end = performance.now();
    console.log(`Tempo para filtrar: ${end - start} ms`);
}
