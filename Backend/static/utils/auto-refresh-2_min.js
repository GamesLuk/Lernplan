document.addEventListener("DOMContentLoaded", function() {
    // Funktion zum Aktualisieren der Daten
    function refreshData() {
        fetch(window.location.href, {
            method: 'GET',
            headers: {
                'Content-Type': 'text/html',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(data => {
            // Ersetze den Inhalt des Body mit den neuen Daten
            const newDocument = new DOMParser().parseFromString(data, 'text/html');
            document.body.innerHTML = newDocument.body.innerHTML;
        })
        .catch(error => console.error('Error:', error));
    }

    // Aktualisiere die Daten alle 2 Minuten (120000 Millisekunden)
    setInterval(refreshData, 1000);
});