# SmartPilot - MESH Hackathon
![Header](pictures/logo.png)

## Kurzfassung

SmartPilot ist ein StartUp, das seines Kunden Planungssicherheit verschafft!

Ein mittels historischen Wetter- und Verkehrsdaten trainiertes Neuronales Netz ermöglicht es, Verkehrsaufkommen zukünftig mit einer höhreren Genauigkeit vorherzusagen. Damit grenzt sich das Produkt SmartPilot von anderen Anbietern ab, die ausschließlich Routenplanung auf Grundlage von Echtzeitdaten durchführen.

## Anwendung
- [`model.py`](model.py): Architektur des [LSTM](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)-Netzes
- [`data.py`](data.py): Datenimport und -aufbereitung für Neuronales Netz 
- [`train.py`](train.py): Start des Trainig Loops und Speichern der [Parameter](model.pth)
- [`predict.py`](predict.py): Bestimmung der Accuracy
- [`smartpilot.py`](smartpilot.py): Vorhersage des Verkehrsaufkommen aufgrundlage von Datum- und Wettervorgabe
- [`webserver.py`](webserver.py): Webserver zur Abfrage von [smartpilot](smartpilot.py)

## Weitere Links

[Challenge](doc/Environmental-Challenge.pdf) / [Prototyp]() / [Neuronales Netz](notebooks/main.ipynb) / [Präsentation](doc/MESH2.pptx) / [smartpilot.ai](https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO)

## Kontakte der Smart Pilots

Alicia Hasselbach <br>
[aliciahasselbach@web.de](mailto:aliciahasselbach@web.de)

Erik Helmut <br>
[erik.helmut1@gmail.com](mailto:erik.helmut1@gmail.com)

Maurice Droll <br>
[mauricedroll@gmail.com](mailto:mauricedroll@gmail.com)

Oliver Gerstl <br>
[oliver.gerstl@web.de](mailto:oliver.gerstl@web.de)