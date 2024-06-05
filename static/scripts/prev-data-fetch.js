// Fetch data from the API
fetch('/api/prev-data')
.then(response => response.json())
.then(data => {
    const dataTable = document.getElementById('dataTable');
    const tbody = dataTable.querySelector('tbody');

    let status_value;

    // Loop through the data and create table rows
    data.forEach(item => {
        if (item.status == "Включення") {
            status_value = "ok"
        } else {
            status_value = "err"
        }

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.status}</td>
            <td>${item.updated}</td>
            <td>${item.interval}</td>
            <!-- Add more cells if needed -->
        `;
        console.log(`status-${status_value}`)
        row.classList.add(`status-${status_value}`);
        tbody.appendChild(row);
    });
})
.catch(error => {
    console.error('Error fetching data:', error);
});