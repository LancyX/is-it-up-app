
async function toggleColumn() {
    const columns = document.querySelectorAll('.toggle-column');
    columns.forEach(column => {
        if (column.style.display === 'none' || column.style.display === '') {
            column.style.display = 'block';
            buttonStatus = "Hide"
        } else {
            column.style.display = 'none';
            buttonStatus = "Hide"
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const columns = document.querySelectorAll('.toggle-column');
    columns.forEach(column => {
        column.style.display = 'none';
    });
});
