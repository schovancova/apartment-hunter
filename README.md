## Scraping tool for apartment finding in Czech Republic

This amazing tool will help you find a new apartment without any hassle,
extra payments, spam or having to subscribe to 10 different paid apartment services.
It's easy.
1. Setup notification methods - you can do phone notifications, desktop notification,
Slack, anything you want - emails do not work currently.
2. Setup filters - What is your budget? All stored in a compact configuration file.
3. Install the app and launch. It can run on your PC, on a server, on a cloud.
4. Get all the sweet apartment notifications for free from most popular apartment sites.

** Please note this currently works only for Brno except for Ulovdomov **

### Usage
#### Setup phone (and desktop) notifications
This can work as a phone-only notifications or desktop too. You can have as many
phones and as many browser included. Here's what you'll need:
1. Download Pushbullet https://play.google.com/store/apps/details?id=com.pushbullet.android
2. Set it up to your liking and create an API access token here https://www.pushbullet.com/#settings
3. Include the token in the environment variable ``export PUSHBULLET_TOKEN=...``
4. Edit ``configs/notifications.ini`` pushbullet section and set ``enabled = true``

#### Setup Slack notifications
If you use Slack at work, this is a perfect choice for you.
1. Create a new Slack workspace (private or work email, does not matter)
2. Go to https://api.slack.com/, create a new app and assign it to your
new workspace.
3. Create a new incoming webhook and assign it to a channel you wish to receive
messages on.
4. Copy webhook URL and put it into environment variable ``export SLACK_WEBHOOK=...``
5. Edit ``configs/notifications.ini`` slack section and set ``enabled = true``

#### How to run the app
After you have enabled and set up at least 1 notification option (and disabled
the ones you don't wish to use), simply run the app:
1. ``pip3 install -r requirements.txt``
2. ``python3 main.py``
3. If you configured things correctly, you should start hearing some notifications.
If not, check the error output.

At this moment you can set filters like 
* price
* size of apartment
* radius (how far from city)
* type of apartment
* which sites to search on

Please note you can leave any config value empty if you 
don't want to filter by it. 

### Websites
* bezrealitky.cz (functional)
* sreality.cz (functional!)
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


### Sreality.cz
Possible config values for "types" option - you can use any combinations,
must be separated by a single comma
* studio
* from 1+1 and 1+kk all the way up 5+1 and 5+kk
* room
* atypical
* 6+

Example: ``types = 1+1,1+kk,atypical,4+kk,6+``
