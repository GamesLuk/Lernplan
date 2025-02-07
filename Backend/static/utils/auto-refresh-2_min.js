// filepath: /c:/Users/lukas/Documents/Programming_Programs/Lernplan/Backend/static/utils/auto-refresh-2_min.js
document.addEventListener("DOMContentLoaded", function() {
    // Funktion zum Aktualisieren der Daten
    function refreshData() {
        const url = new URL(window.location.href);
        url.searchParams.set('cache_bust', Date.now()); // Cache-Busting-Parameter hinzufügen

        fetch(url, {
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

            // Aktualisiere das eingebettete CSS
            const styles = newDocument.querySelectorAll('style');
            document.querySelectorAll('style').forEach((style, index) => {
                if (styles[index]) {
                    style.innerHTML = styles[index].innerHTML;
                }
            });
        })
        .catch(error => console.error('Error:', error));
    }

    // Aktualisiere die Daten alle 2 Minuten (120000 Millisekunden)
    setInterval(refreshData, 1000 * 60 * 2);
});