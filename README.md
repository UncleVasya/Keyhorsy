# Keyhorsy
Scripts to parse data from dota league matches.

## Installation:

1. Get the code.
2. Open cmd in a code folder.
3. Setup virtualenv:

```
pip install virtualenv
virtualenv .virtualenv
```

4. Activate virtualenv:
```
.virtualenv\Scripts\activate.bat
```

5. Download project dependencies:
```
pip install -r requirements.txt
```

6. Create database:
```
python manage.py migrate
```

7. Create an admin user for db
```
python manage.py createsuperuser
```

## How to use:

1. First download the list of dota heroes:
```
python manage.py get_heroes
```

2. Now you can download data for your desired league:
```
python manage.py get_league_data 13515
```

After these steps you will have a database with league players, matches and teams that you can use query for stats.

To update database with new matches just use the script again.

You can download data for multiple leagues by using `get_league_data` with other leagues ids.

3. You can see database data in Django admin panel:
```
python manage.py runserver
```
Then open `http://127.0.0.1:8000/admin` in browser and login with your superuser credentials.
