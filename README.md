# Web-App-Server - Todo-Listen Verwaltung

## 1 Erstellung des Servers in Virtual Box
    -Ziel eine VM Erstellen die den Anforderungen entspricht

### Name und Betriebsystem der Virtuellen Maschine
    -VM-Name: Web-App
    -VM-Ordner: C:\Users\Niestegge\VirtualBox VMs
    -ISO-Abbild: C:\Users\Niestegge\Downloads\ubuntu-26.04-live-server-amd64.iso
        -Betriebsystem: Linux
        -Betriebsystem-Distribution: Ubuntu
        -Betriebsystem-Version: Ubuntu 25.04 (Plucky Puffin) (64-Bit)

### Einrichtung der unbeaufsichtigten Installation des Gastbetriebsystems
    -Benutzername: server

### Virtuelle Hardware angeben
    -Hauptspeicher: 4096 MB (4 GB)
    -Anzahl der CPUs: 6

### Virtuelle Festplatte angeben
    -Plattenabbildort: C:\Users\Niestegge\VirtualBox VMs\Web-App\Web-App.vdi
    -Plattenabbildgroesse: 50 GB

## 2 Installation der VM
    -Ziel: Die VM einmal anschalten und keine Fehler haben, dazu eine deutsche Eingabe

### Start
    -VM Web-App-Server starten
    -Installation startet automatisch

    -Nach abschluss Anmelden als Benutzer server

### Tastaturlayout umstellen auf Deutsch
    -bash: "sudo dpkg-reconfigure keyboard-configuration" (Gibt einem die Wahl des Tastaturlayouts)
            -Auswahl: Generic 105-key PC
            -Auswahl: German
            -Auswahl: German
            -Rest: Standart

    -Nach dem naechsten Neustart hat die Tastatur ein deutsches Layout
    -bash: "setupcon" (Wenn man das Layout direkt anwenden will)

### Herunterfahren
    -bash: "sudo shutdown -h now" (System herunterfahren)

## 3 Netzwerk konfigurieren
    -Ziel: Statische IP-Adresse erstellen

### Anpassungen in VirtualBox
    -VM Auswaehlen -> Aendern -> Netzwerk -> Adapter 1
    -Anpassen:
        -Angeschlossen an: Netzwerkbruecke
        -Name: <Verwendete Netzwerkkarte> 
    (Das Geraet war waehrend der Einrichtung per LAN-Kabel mit meinem Heimnetzwerk verbunden.)
    
    -Speichern, Schliessen, VM starten, Anmelden

### Pruefen der aktuellen IP
    -bash: "ip a" (Anzeigen der eigenen IP Informationen)
    -bash: "ip route" (Anzeigen der Netzadresse)
    -Ergebnis:
        -Interface: enp0s3
        -DHCP-Addresse: 192.168.123.68
    
### Statische IP-Adresse einrichten
    -bash: "sudo nano /etc/netplan/00-installer-config.yaml" (Bearbeiten der Pfaddatei (der Netzplan))
    -Anpassen zu: (
            network:
                version: 2
                ethernets:
                    enp0s3:
                        dhcp4: false
                        addresses:
                            - 192.168.24.104/24
                        routes:
                            - to: default
                              via: 192.168.24.254
                        nameservers:
                            addresses:
                                - 192.168.24.254
                                - 8.8.8.8   
    )
    - Danach: Strg + O , Enter, Strg + X

    -bash: "sudo netplan try" (Testet den erstellen Netzplan)
    -Danach: Enter

### Statische IP-Adresse Pruefen
    -bash: "ip a" (Zeigt die Eigene Netzwerkverbindung an)
    -bash: "ip route" (Zeigt die Netzadresse)
    -Ergebnis:
        -Interface: enp0s3
        -DHCP-Addresse: 192.168.24.104

## 4. Erstellen der Benutzer
    -Ziel: Benutzer willi ohne Adminrechte, Benutzer fernzugriff mit Adminrechten erstellen

### Erstellung vom Benutzer willi
    -bash: "sudo adduser willi" (Erstellen von Benutzer willi)
    -Danach koennen Namen, Raum usw. angegeben werden, oder die Felder einfach mit Enter leer gelassen werden
    -Bestaetigen mit: "Y"

    -Pruefen der Rechte:
    -bash: "id willi" (Auslesen der Benutzerid und Benutzergruppen)
    -Ergebnis: Keine Adminrechte

### Erstellung vom Benutzer fernzugriff
    -bash "sudo adduser fernzugriff" (Erstellen von Benutzer Fernzugriff)

    -bash "sudo usermod -aG sudo fernzugriff" (Hinzufuegen der Benutzergruppe sudo zu fernzugriff)

    -bash "id fernzugriff" (Auslesen der Benutzerid und Benutzergruppen)
    -Ergebnis: Adminrechte

## 5. SSH Installieren
    -Ziel: SSH installieren, damit der Benutzer fernzugriff, SSH nutzen kann.

### Installation starten
    -bash: "sudo apt update" (Informationen zu updates erhalten)
    -bash: "sudo apt install openssh-server -y" (Installiert SSH)
    -bash: "sudo systemctl status ssh" (Gibt den SSH status aus)
    -Ergebnis: 
        -enabled

## 6. SSH Einrichten
    -Ziel: Benutzer fernzugriff soll SSH nutzen koennen

### Verbindung hinzufuegen
    -bash: "ssh fernzugriff@192.168.24.104" (Die SSH Verbindung bei fernzugriff hinzufuegen)
    -bash: "yes" (bestaetigen)
    -Anmelden mit fernzugriff

### Benutzer auf server wechseln
    -bash: "sudo su - server" (Benutzerwechsel forcen auf Benutzer server)

## 7. Python und Docker installieren
    -Ziel: Python ist installiert und funktionsfaehig

### Installation Python
    -bash: "sudo apt install python3-flask -y" (Installation von Python 3 starten)

### Installation Docker
    -bash: "sudo apt install docker.io -y" (Installation von Docker)

### Starten von Docker
    -bash: "sudo systemctl enable docker" (Aktivieren von Docker)
    -Bestaetigen mit Benutzer Server

    -bash: "sudo systemctl start docker" (Docker starten)

## 8. Todo-Web-App bereitstellen
    -Ziel die Web-App liegt auf dem Server und ist ueber die statische IP erreichbar

### Wechseln des Benutzers
    -bash: "su - fernzugriff" (anmelden als fernzugriff)

### Erstellen von einem Verzeichnis
    -bash: "mkdir ~/todo-app (Erstellen eines Ordners im Benutzerpfad (= ~) von fernzugriff)
    -bash: "cd ~/todo-app (navigieren in den Pfad)

### Web-App per Powershell verschieben
    -Terminal im Git-Verzeichnis oeffnen, wo die Datei liegt
    -Befehl: "scp Web-App.py fernzugriff@192.168.123.100:/home/fernzugriff/todo-app/"
    -Danach wieder auf den Server wechseln

## 9. Python App starten
    -Ziel: Testen, dass die App startet

### Starten
    -bash: "python3 Web-App.py" (Starten der App)
    -Ergebnis: Running on http://192.168.24.104:5000/todo-list
    -App ist aufrufbar

    - Strg + C (Beenden der App)

## 10. Docker einrichten
    -Einen Container erstellen, der Automatisch hochfaehrt, ausser er wurde beendet

### requirements.txt erstellen
    -bash: "nano requirements.txt" (erstellt das Dokument und oeffnet die Bearbeitung)
    -Inhalt: (
        flask
    )
    -danach Strg + O, Enter, Strg + X

### dockerfile erstellen
    -bash: "nano dockerfile" (Erstellt die Datei mit Bearbeitung)
    -Inhalt: (
        FROM python:3.12-slim
        WORKDIR /app
        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt
        COPY Web-App.py .
        EXPOSE 5000
        CMD ["python", "Web-App.py"]
    )
    -danach Strg # O, Enter, Strg + X

### Docker image bauen
    bash: "sudo docker build -t todo-app ." (Container wird vorbereitet)
    bash: "sudo docker run -d --name todo-container -p 5000:5000 todo-app" (erstellt und startet den Container)
    bash: "sudo docker ps" (zeigt einem die Container die aktuell laufen)

### Container verwalten
    bash: "sudo docker stop todo-container" (stoppen)
    bash: "sudo docker start todo-container" (starten)
    bash: "sudo docker ps" (Informationen zu laufenden Containern anzeigen)

## 11. Programm im Web aufrufen

    Browser eines Geraets im selben Netzwerk
    Link: http://192.168.24.104:5000/todo-list
