import fetchTitles from '/static/scripts/titles.js';
import fetchNav from '/static/scripts/nav.js';
import fetchTranslation from '/static/scripts/translations.js';

async function fetchData() {
    await fetchTitles()
    await fetchNav("table")

    const response = await fetch('/api/table');
    const data = await response.json();

    const dataTable = document.getElementById('dataTable');
    const tbody = dataTable.querySelector('tbody');

    const translation = await fetchTranslation("table")

    document.getElementById('legend').innerHTML = '<h3>' + translation.legend + '</h3>';

    document.getElementById('text').innerHTML = '<li class="text"><strong>' + translation.interval + '</strong> - '
        + translation.interval_text + '</strog> '
        + '<a class="status-ok"><strong>' + translation.legend_on + '</strong></a> / ' +
        '<a class="status-err"><strong>' + translation.legend_off + '</strong></a>';

    document.getElementById('text').innerHTML = '<li class="text"><strong>' + translation.interval + '</strong> - '
        + translation.interval_text + '</strog> '
        + '<a class="status-ok"><strong>' + translation.legend_on + '</strong></a> / ' +
        '<a class="status-err"><strong>' + translation.legend_off + '</strong></a>';

    document.getElementById('status').innerHTML = '<th>' + translation.status + '</th>';
    document.getElementById('day').innerHTML = '<th>' + translation.day + '</th>';
    document.getElementById('time').innerHTML = '<th>' + translation.time + '</th>';
    document.getElementById('interval').innerHTML = '<th>' + translation.interval + '</th>';

    let status_value;
    let status_text;

        data.forEach(item => {
            if (item.status == "OK") {
                status_value = "ok"
                status_text = translation["legend_on"]
            } else {
                status_value = "err"
                status_text = translation["legend_off"]
            }

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${status_text}</td>
                <td>${item.day_of_week}</td>
                <td>${item.inserted}</td>
                <td>${item.interval}</td>
            `;
            row.classList.add(`status-${status_value}`);
            tbody.appendChild(row);
        })
    }

window.onload = fetchData;