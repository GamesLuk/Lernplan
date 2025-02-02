$r1 = "C:\Users\lukas\Documents\Programming_Programs\Lernplan\Zusatz\run\r1.ps1"
$r2 = "C:\Users\lukas\Documents\Programming_Programs\Lernplan\Zusatz\run\r2.ps1"
$r3 = "C:\Users\lukas\Documents\Programming_Programs\Lernplan\Zusatz\run\r3.ps1"
$r4 = "C:\Users\lukas\Documents\Programming_Programs\Lernplan\Zusatz\run\r4.ps1"
$r5 = "C:\Users\lukas\Documents\Programming_Programs\Lernplan\Zusatz\run\r5.ps1"
$r6 = "C:\Users\lukas\Documents\Programming_Programs\Lernplan\Zusatz\run\r6.ps1"

wt -w 0 nt -p "PowerShell" --title "Tunnel" -d . powershell -NoProfile -ExecutionPolicy Bypass -File "$r1"
wt -w 0 nt -p "PowerShell" --title "Caddy" -d . powershell -NoProfile -ExecutionPolicy Bypass -File "$r2"
wt -w 0 nt -p "PowerShell" --title "Django" -d . powershell -NoProfile -ExecutionPolicy Bypass -File "$r3"
wt -w 0 nt -p "PowerShell" --title "Redis" -d . powershell -NoProfile -ExecutionPolicy Bypass -File "$r4"
wt -w 0 nt -p "PowerShell" --title "Celery" -d . powershell -NoProfile -ExecutionPolicy Bypass -File "$r5"
wt -w 0 nt -p "PowerShell" --title "Celery - Beat" -d . powershell -NoProfile -ExecutionPolicy Bypass -File "$r6"

Stop-Process -Id $PID