async function fetchTranslation(page) {
    const headers = {
        'Content-Type': 'application/json',
       };
    const response_translation = await fetch('/api/translation', { method: 'POST', headers: headers, body: JSON.stringify({ "page": page }) });
    const translation = await response_translation.json();
    return translation
}

export {fetchTranslation as default};
