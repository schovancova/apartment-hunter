## Scraping tool for apartment finding in Czech Republic

### Usage
1. Create throw-away email gmail account for sending emails
2. Edit all configs, replace with your emails and values
3. Put your new gmail account email into environment variable ``export EMAIL_PASS=...``
4. ``pip3 install -r requirements.txt``
5. You should see emails on your main account now, leave app running on
server or locally to receive new offers from all sites!

At this moment you can set filters like 
* price
* size of apartment
* radius (how far from city)
* type of apartment
* which sites to search on 
* lack of commission in offers FOR FREE (for ulovdomov)

Please note you can leave any config value empty if you 
don't want to filter by it. 

### Websites
* bezrealitky.cz (functional)
* sreality.cz (TBD)
* ulovdomov.cz (functional)

### Ulovdomov.cz
Possible config values for "types" option - you can use any combinations,
must be separated by a single comma
* studio
* from 1+1 and 1+kk all the way up 4+1 and 4+kk
* atypical, house, 5+, room

Example: ``types = studio,house,3+1,atypical``

### Bezrealitky.cz
Possible config values for "types" option - you can use any combinations,
must be separated by a single comma
* studio
* from 1+1 and 1+kk all the way up 7+1 and 7+kk
* other

Example: ``types = 1+1,1+kk,other,4+kk``

Possible config values for "offer_type" option - use just 1
* rent
* sharing
* sale

