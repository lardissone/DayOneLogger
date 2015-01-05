# DayOneLogger

Log anything you add to a folder to Day One. Ideal to use with IFTTT. Inspired in [Sifttter](http://craigeley.com/01-07-2014/sifttter-an-ifttt-to-day-one-logger/) and [Slogger](http://brettterpstra.com/projects/slogger/).

## How does it works

**DayOneLogger** is an script that runs daily (or in the time period you define) and automatically checks for new entries on different files in the defined directory.
The files must contain an specific format:

    <date>|~|<any extra content defined by the parsers>@done

The date need to be in the format `September 05, 2014 at 03:06PM` (the one used by IFTTT).
The separator `|~|` is just to separate each content of the entry. You can add as many separators as you need, later the parser will do the magic understanding what each content means.
And finally you need to add the ending token identified as `@done`, to inform the parsers where an entry finish.

Example from a completed reminder in Reminders iOS app:

    September 05, 2014 at 03:05PM|~|Reminders|~|Buy milk @done

The script only stores on Day One all entries from previous day and before, it's intentionally done to avoid miss last time entries.

It also logs previous unimported days.

The resulting entry looks like:
![](http://i.imgur.com/RfnurZ4.png)

## Installation

Clone the repository:

    git clone https://github.com/lardissone/DayOneLogger.git

The only requirement is the beautiful [Arrow](http://crsmithdev.com/arrow/) library, but if you want more control you can install it using a `virtualenv`.

Install requirements (requires `pip`):

    pip install -r requirements.txt

## Configuration

You need to edit a few settings in the source of the `dayone.py` file:

- `IFTTT_DIR`: set the relative directory to where you store the logging files
- `DAYONE_DIR`: uncomment the corresponding option. If you have syncing with iCloud or Dropbox.
- `TIME_ZONE`: set your local timezone to include the correct time. You can find the list of all timezones in [Wikipedia](http://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Note: it should be automatic, but `tzlocal` library doesn't works well in OSX with some specific zones.
- `TIME_ZONE_OFFSET`: it's the number of difference in hours from `UTC`. It's also something we should calculate automatically, probably in the future.
- `ENTRY_TAGS`: a list with the tags to be used in each entry.

- `SERVICES`: a list with the services you want to process. Review each service file in the `services` folder in case you need to do custom modifications, actual services are:

    SERVICES = [
        'github',
        'reminders',
        'movies',
        'places',
        'tracks',
        'tweets',
        'wakatime',
        'todoist',]

To run the script you just need to call it from the terminal by using:

    python dayone.py

To make it effective you should add it to a cron or launchd script.

## Parsers

Currently here are a few of parsers I've created for my pleasure, all of them uses [IFTTT](https://ifttt.com/) to generate the data from my other services.

You can simply use any of these recipes with your services. Remember to change the settings according to your setup.

### Github

Use your activity atom feed URL, which is: `https://github.com/yourusername.atom`

<a href="https://ifttt.com/view_embed_recipe/201733-dayonelogger-github-to-dropbox" target = "_blank" class="embed_recipe embed_recipe-l_31" id= "embed_recipe-201733"><img src= 'https://ifttt.com/recipe_embed_img/201733' alt="IFTTT Recipe: DayOneLogger: Github to Dropbox connects feed to dropbox" width="370px" style="max-width:100%"/></a><script async type="text/javascript" src= "//ifttt.com/assets/embed_recipe.js"></script>

### Reminders (iOS app)

Log all your completed tasks in the Reminders app. You need the IFTTT app installed in your phone.

<a href="https://ifttt.com/view_embed_recipe/201734-dayonelogger-reminders-to-dropbox" target = "_blank" class="embed_recipe embed_recipe-l_34" id= "embed_recipe-201734"><img src= 'https://ifttt.com/recipe_embed_img/201734' alt="IFTTT Recipe: DayOneLogger: Reminders to Dropbox connects ios-reminders to dropbox" width="370px" style="max-width:100%"/></a><script async type="text/javascript" src= "//ifttt.com/assets/embed_recipe.js"></script>

### Twitter

Log all your Twitter activity.

<a href="https://ifttt.com/view_embed_recipe/201738-dayonelogger-tweets-to-dropbox" target = "_blank" class="embed_recipe embed_recipe-l_31" id= "embed_recipe-201738"><img src= 'https://ifttt.com/recipe_embed_img/201738' alt="IFTTT Recipe: DayOneLogger: Tweets to Dropbox connects twitter to dropbox" width="370px" style="max-width:100%"/></a><script async type="text/javascript" src= "//ifttt.com/assets/embed_recipe.js"></script>

### IMDb rated movies

It's a little more tricky to obtain. Log in to IMDb, and go to your Ratings, and you'll see the feed icon to the upper right of the page, use this URL.

<a href="https://ifttt.com/view_embed_recipe/201735-dayonelogger-imdb-rated-movies-to-dropbox" target = "_blank" class="embed_recipe embed_recipe-l_42" id= "embed_recipe-201735"><img src= 'https://ifttt.com/recipe_embed_img/201735' alt="IFTTT Recipe: DayOneLogger: IMDb rated movies to Dropbox connects feed to dropbox" width="370px" style="max-width:100%"/></a><script async type="text/javascript" src= "//ifttt.com/assets/embed_recipe.js"></script>

### Foursquare

Log all the places you visits.

<a href="https://ifttt.com/view_embed_recipe/201736-dayonelogger-add-check-ins-to-dropbox" target = "_blank" class="embed_recipe embed_recipe-l_38" id= "embed_recipe-201736"><img src= 'https://ifttt.com/recipe_embed_img/201736' alt="IFTTT Recipe: DayOneLogger: Add Check-ins to Dropbox connects foursquare to dropbox" width="370px" style="max-width:100%"/></a><script async type="text/javascript" src= "//ifttt.com/assets/embed_recipe.js"></script>

### Last.fm loved tracks

Log all your loved tracks.

<a href="https://ifttt.com/view_embed_recipe/201737-dayonelogger-loved-track-to-dropbox" target = "_blank" class="embed_recipe embed_recipe-l_36" id= "embed_recipe-201737"><img src= 'https://ifttt.com/recipe_embed_img/201737' alt="IFTTT Recipe: DayOneLogger: Loved track to Dropbox connects last-fm to dropbox" width="370px" style="max-width:100%"/></a><script async type="text/javascript" src= "//ifttt.com/assets/embed_recipe.js"></script>


### Todoist completed tasks

Log all the tasks you've completed.

<a href="https://ifttt.com/view_embed_recipe/231068-dayonelogger-todoist-to-dropbox" target = "_blank" class="embed_recipe embed_recipe-l_32" id= "embed_recipe-231068"><img src= 'https://ifttt.com/recipe_embed_img/231068' alt="IFTTT Recipe: DayOneLogger: Todoist to Dropbox connects todoist to dropbox" width="370px" style="max-width:100%"/></a><script async type="text/javascript" src= "//ifttt.com/assets/embed_recipe.js"></script>

### Wakatime worked hours

Log how much time did you spend in each project using [Wakatime](https://wakatime.com/).

You need to create an environment variable called `WAKATIME_API_KEY` with your Wakatime API key, or add it to the `services/wakatime.py` file.


## TO DO

- Add tests
- Add documentation about launchd, cron, etc.
- Isolate parsers
- Allow editing previous entries
- Find a way to get current timezone in OSX. `tzlocal` library is pretty buggy with some locations


## Author

This simple script was created by [Leandro Ardissone](https://github.com/lardissone). Feel free to contact me on [Twitter](http://twitter.com/Leech) or leave [issues](https://github.com/lardissone/DayOneLogger/issues) in github with suggestions/bugs/etc.
