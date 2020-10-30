## Scraping tool for apartment finding in Czech Republic

### Usage
1. Create throw-away email gmail account for sending emails
2. Edit all configs, replace with your emails and values
3. Put your new gmail account email into environment variable ``export EMAIL_PASS=...``
4. ``pip3 install -r requirements.txt``
5. You should see emails on your main account now, leave app running on
server or locally to receive new offers from all sites for free!

### Websites
* bezrealitky.cz (TBD)
* sreality.cz (TBD)
* ulovdomov.cz (functional)

### Ulovdomov.cz
Possible config values for "types" option - you can use any combinations,
must be separated by a single comma
* garsonka
* 1+kk, 1+1 
* 2+kk, 2+1
* 3+kk, 3+1
* 4+kk, 4+1
* atypický, dům, 5 a větší
* Sdílený pokoj

Example of types config for some who wants either 3 rooms or a house:
``types = 3+1,4+kk,dům``

