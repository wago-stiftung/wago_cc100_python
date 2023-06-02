# CC100IO

Basic python module to control the input and output ports of a WAGO CC100. Module can be used native on device or in Docker Container

## Contributors
- Konrad Holsmoelle <konrad.holsmoelle@wago.com>
- Bjarne Zaremba <bjarne.zaremba@wago.com>
- Tobias Pape <tobias.pape@wago.com>
- Tobias Schaekel <tobias.schaekel@wago.com>
- Mattis Schrade <mattis.schrade@wago.com>
- Bekim Imrihor <bekim.imrihor@wago.com>
- Nele Stocksmeyer <nele.stocksmeyer@wago.com>
- Sascha Hahn <sascha.hahn@wago.com> 
- Danny Meihoefer <danny.meihoefer@wago.com>


## 1. CC100 vorbereiten
### 1. feste IP auf USB-Ethernet-Adapter konfigurieren
1. Windowseinstellungen öffnen --> Netzwerk und Internet --> Adaptereinstellungen ändern
2. Rechtsklick auf USB-Adapter --> Eigenschaften
3. Doppelklick auf "internetprotokoll, Version 4"
4. IP-Adresse: 192.168.1.xx (z.B. 192.168.1.10)
5. Subnetzmaske: 255.255.255.0

### 2. temporäre IP auf CC100 konfigurieren
1. Betriebsartenschalter in STOP-Position
2. Reset-Taster (RST) länger als 8 Sekunden drücken
Die Ausführung wird durch eine orange blinkende „SYS“-LEDs signalisiert. Hiermit wurde dem CC100 die temporäre IP 192.168.1.17 zugewiesen.

### 3. CC100 konfigurieren
1. Ethernetkabel an Steckplatz X1 des CC100
2. IP-Adresse des CC100 in Adressleiste des Webbrowser eingeben um auf das WBM zu gelangen
3. Anmeldedaten des CC100
- Benutzer: admin
- Kennwort: wago
4. Wenn Anfrage für Kennwortänderung angezeigt wird abbrechen
5. auf Startseite prüfen, ob Firmware Revision 21 oder größer ist
6. feste IP Adresse einstellen
- Configuration --> Networking
- IP Source: Static IP
- Static IP Adress kann auf 17 bleiben
- Subnetzmaske kann bleiben
- Submit
7. Uhrzeit einstellen (falls erforderlich)
- Configuration --> Clock


### Installation von Python 3.7 auf dem CC100
Es befindet sich bereits eine Python Installation auf dem Gerät (Version 2.7). Es wird allerdings Version 3.7 benötigt.

1. IPK-Datei herunterladen (https://github.com/WAGO/cc100-howtos/blob/main/HowTo_AddPython3/packages/python3_3.7.6_armhf.ipk)
2. über das WBM Python installieren
- Configuration --> Software Uploads
- zuvor heruntergeladene IPK auswählen und installieren

## Nutzung von Python auf dem CC100
Um Pythoncode auf dem CC100 schreiben und ausführen zu können, muss der Zugriff mit dem Linux Betriebssystem auf dem Gerät
hergestellt werden können. Dafür bietet sich eine Verbindung über SSH an. SSH stellt eine verschlüsselte Verbindung in Form
eines Terminals zur Verfügung. Der CC100 unterstützt dies standardmäßig. Mac- und Linux-PC unterstützen i.d.R. ebenfalls bereits SSH.
Unter Windows muss zunächst ein SSH-Client installiert werden.

### SSH-Client auf Windows-PC installieren
1. Apps und Features öffnen --> Feature hinzufügen
2. SSH eingeben --> OpenSSH-Client installieren
3. Kommandozeile öffnen (cmd)
```bash
ssh root@192.168.1.17 
```
- password: wago
4. Python Installation prüfen
```bash
python3
```

### Visual Studio Code konfigurieren
1. https://code.visualstudio.com/download
2. Python Extension installieren (ms-python.python)
3. SSH Client Extension installieren, z.B. thangnc.ssh-client
- add Connection

### Python-Bibliothek zum Ansteuern der Ein- und Ausgänge installieren
1. Dieses Repository herunterladen
2. In das Verzeichnes des Repositories wechseln und Kommandozeile öffnen
```bash
scp -pr ./CC100IO root@192.168.1.17:/home/python_scripts
```

Die Pythonsscripts können nun im Verzeichnis python_scripts erstellt werden. Es muss lediglich das
CC100IO Modul in den Pythonscripts importiert werden.


## Example
```python
import CC100IO
def armHoch():

    CC100IO.digitalWrite(True, 3)
    if CC100IO.digitalReadWait(4, False):
        CC100IO.digitalWrite(False, 3)
        return True
```

## Description of functions

* #### ```digitalWrite (value, output)``` :
  * value: Value which the selected output should be set to (True or False)
  * output: Digital output to be switched (1-4)
  * Function switches the output to the specified value.
  * Function does not check the current value of the output.
  * Function returns True if value is written, returns False if an error occured. 
* #### ```analogWrite (voltage, output)``` : 
  * voltage: Voltage which the selected output should be set to (0 - 10000 mV)
  * output: Analog output to be switched(1 or 2)
  * Function switches the output to the specified voltage. 
  * Function does not check the current value of the output. 
  * Function returns True if value is written, returns False if an error occured. 
* #### ```digitalRead (input)``` :
  * input: Digital input to be read (1-8)
  * Function reads the input. 
  * Function does not check the current value of the output. 
  * Returns True or False depending on the value.
* #### ```digitalReadWait (input, value)``` :  
  * input: Digital input to be checked (1-8)
  * value: State to be queried at the input
  * Reads the specified input until the desired state is reached, by another Function or external factors and then returns True.
  * Function runs until the state is reached.
* #### ```analogRead (input)``` :
  * input: Analog input to be read (1 or 2)
  * Function reads the input and returns the calibrated value in mV as an Integer.
* #### ```delay (iTime)``` :
  * Function makes the programm in a period of time late or slow. (in ms)
* #### ```tempRead (input)``` :
  *  input: PT input to be switched ("PT1" or "PT2")
  *  Function reads the input and returns the calibrated value in °C as an Integer.


