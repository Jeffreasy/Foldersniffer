
# FolderSniffer Dashboard

FolderSniffer is een applicatie voor het visualiseren van bestandstype distributies, bestandsgrootte analyses, en tijdlijnen van bestand modificaties binnen een specifieke directory. Dit project maakt gebruik van PyQt6 voor de GUI en Matplotlib en Seaborn voor de grafieken.

## Inleiding

De FolderSniffer dashboard applicatie biedt een intuïtieve grafische gebruikersinterface (GUI) voor het analyseren en visualiseren van bestanden in een specifieke map. De applicatie toont grafieken met betrekking tot bestandstypen, bestandsgroottes en de tijdlijn van bestandmodificaties.

## Installatie

Volg de onderstaande stappen om het project lokaal op te zetten:

```bash
# Clone de repository
git clone https://github.com/yourusername/foldersniffer.git

# Navigeer naar de projectmap
cd foldersniffer

# Installeer de vereiste pakketten
pip install -r requirements.txt
```

## Gebruik

Instructies voor het gebruik van de applicatie:

```python
# Voer de applicatie uit
python main.py
```

## Componenten Beschrijving

### Dashboard Component

Het `Dashboard` component is verantwoordelijk voor het weergeven van verschillende statistieken en grafieken met betrekking tot bestanden in de geselecteerde directory. Het bevat de volgende functionaliteiten:

- **Bestandstype Grafiek**: Toont de verdeling van verschillende bestandstypen in een cirkeldiagram.
- **Bestandsgrootte Grafiek**: Toont de verdeling van bestandsgroottes in een staafdiagram.
- **Bestandswijziging Tijdlijn**: Visualiseert de tijdlijn van bestandmodificaties.
- **Bestandsevenementen Grafiek**: Toont het aantal verschillende bestandsevenementen zoals aangemaakt, gewijzigd, en verwijderd.
- **Samenvatting**: Geeft een overzicht van het totale aantal bestanden, de totale grootte, en de gemiddelde bestandsgrootte.

Het `Dashboard` maakt gebruik van PyQt6 widgets zoals `QLabel`, `QGridLayout`, `QScrollArea`, `QTableWidget` en `QPushButton`. Het maakt ook gebruik van `matplotlib` en `seaborn` voor het plotten van grafieken en diagrammen.

## Contributing

Bijdragen aan dit project zijn welkom. Volg de standaard werkwijze voor forking de repository, het maken van een nieuwe branch, het aanbrengen van wijzigingen en het indienen van een pull request.

## Licentie

Dit project is gelicentieerd onder de MIT License - zie het LICENSE bestand voor details.
