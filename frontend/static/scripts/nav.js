import fetchTranslation from '/static/scripts/translations.js';

async function fetchNav(title) {
    const translation = await fetchTranslation("titles");

    document.getElementById("title").innerHTML = translation[title];

    document.getElementById('main').innerHTML = '<a href="/">' + translation["main"] + '</a>';
    document.getElementById('table').innerHTML = '<a href="/table">' + translation["table"] + '</a>';
    document.getElementById('contacts').innerHTML = '<a href="/contact">' + translation["contacts"] + '</a>';

}

export { fetchNav as default};
