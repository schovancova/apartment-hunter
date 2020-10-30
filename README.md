## Scraping tool for apartment finding in Czech Republic

### Usage
1. Create throw-away email gmail account for sending emails
2. Edit all configs, replace with your emails and values
3. Put your new gmail account email into environment variable ``export EMAIL_PASS=...``
4. ``pip3 install -r requirements.txt``
5. You should see emails on your main account now, leave app running on
server or locally to receive new offers from all sites for free!

### Websites
* bezrealitky.cz (functional)
* sreality.cz (TBD)
* ulovdomov.cz (functional)

### Ulovdomov.cz
Possible config values for "types" option - you can use any combinations,
must be separated by a single comma
* studio
* from 1+1 and 1+kk all the way up 4+1 and 4+kk
* atypical,house,5+,room

### Bezrealitky.cz
Possible config values for "types" option - you can use any combinations,
must be separated by a single comma
* studio
* from 1+1 and 1+kk all the way up 7+1 and 7+kk
* other

Possible config values for "offer_type" option - use just 1
* pronajem
* spolubydleni
* prodej

