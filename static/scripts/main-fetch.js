async function fetchData() {
    const response = await fetch('/api/main');
    const data = await response.json();
    let power_text;
    if (data.power == "OK") {
        power_text = 'Наявне впродовж'
    } else {
        power_text = 'Відсутнє впродовж'
    }

    let last_power_text;
    if (data.power == "OK") {
        last_power_text = 'Було відсутнє впродовж'
    } else {
        last_power_text = 'Було наявне впродовж'
    }

    document.getElementById('power').innerHTML = '<strong>' + power_text + '</strong>: ' + data.interval;
    document.getElementById('timestamp').innerHTML = '<strong>Дані оновлено</strong>: ' + data.timestamp;
    document.getElementById('interval').innerHTML = '<strong>' + last_power_text + '</strong>: ' + data.interval_previous;
    document.getElementById('last_power_on').innerHTML = '<strong>Останнє включення</strong>: ' + data.last_power_on;
    document.getElementById('last_power_off').innerHTML = '<strong>Останнє відключення</strong>: ' + data.last_power_off;
    const img = document.getElementById('power_img');
    img.src = data.power == "OK" ? '/static/img/power-on.png' : '/static/img/power-off.png';
}

setInterval(fetchData, 30000);  // Fetch data every 30 seconds
window.onload = fetchData;