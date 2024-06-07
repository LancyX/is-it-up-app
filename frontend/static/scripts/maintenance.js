import fetchTranslation from '/static/scripts/translations.js';

async function fetchData() {

    const translation = await fetchTranslation("maintenance")

    document.getElementById('title').innerHTML = translation.title;
    document.getElementById('title_small').innerHTML = '<h2>' + translation.title + '</h2>';
    document.getElementById('text').innerHTML = '<p><strong>' + translation.text + '</strong></p>';
}

window.onload = fetchData;
