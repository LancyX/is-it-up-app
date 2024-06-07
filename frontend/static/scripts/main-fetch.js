import fetchTitles from '/static/scripts/titles.js';
import fetchNav from '/static/scripts/nav.js';
import fetchTranslation from '/static/scripts/translations.js';

async function fetchData() {
    await fetchTitles()
    await fetchNav('main')

    const translation = await fetchTranslation("main");

    const response = await fetch('/api/main');
    const data = await response.json();


    let status_text;
    let last_status_text;

    if (data.status == "OK") {
        status_text = translation.status_on
        last_status_text = translation.prev_status_off
    } else {
        status_text = translation.status_off
        last_status_text = translation.prev_status_on
    }

    document.getElementById('status').innerHTML = '<strong>' + status_text + '</strong>: ' + data.interval;
    document.getElementById('timestamp').innerHTML = '<strong>' + translation["time"] + '</strong>: ' + data.timestamp;
    document.getElementById('current').innerHTML = '<strong>' + translation["current"] + '</strong>: ';
    document.getElementById('prev').innerHTML = '<strong>' + translation["prev"] + '</strong>: ';
    document.getElementById('interval').innerHTML = '<strong>' + last_status_text + '</strong>: ' + data.interval_previous;
    document.getElementById('last_on').innerHTML = '<strong>' + translation["last_on"] + '</strong>: ' + data.last_on;
    document.getElementById('last_off').innerHTML = '<strong>' + translation["last_off"] + '</strong>: ' + data.last_off;
    const img = document.getElementById('power_img');
    img.src = data.status == "OK" ? '/static/img/power-on.png' : '/static/img/power-off.png';
}

setInterval(fetchData, 30000);  // Fetch data every 30 seconds
window.onload = fetchData;
