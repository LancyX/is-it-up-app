async function fetchTitles() {

    const response_titles = await fetch('/api/titles');
    const titles = await response_titles.json();
    
    document.getElementById('title_1').innerHTML = '<h3>' + titles["title_1"] + '</h3>';
    document.getElementById('title_2').innerHTML = '<h3>' + titles["title_2"] + '</h3>';

}

export { fetchTitles as default};
