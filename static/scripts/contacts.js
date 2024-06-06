import fetchNav from '/static/scripts/nav.js';
import fetchTranslation from '/static/scripts/translations.js';

async function fetchData() {
    await fetchNav("contacts")

    const translation = await fetchTranslation("titles")
    document.getElementById('title_small').innerHTML = '<h2>' + translation.contacts + '</h2>';
}

window.onload = fetchData;