# EQ weather application local deployment guide

Tested with Python 3.10.

It will probably work just fine with later Python versions, but no promises.

## Installation

Make sure you have Python module venv installed and do:

```
git clone git@github.com:Goury/eqweather.git
cd eqweather
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 
./manage.py makemigrations
./manage.py migrate
```

## US Weather API querying

### Discovering grid cells

Firstly, grab yourself a map and find a recrangular region you're interested in.

Then find latitude and longitude values for its corners and run this command to query all the grid cells in the area:

```
./manage.py query_cells --lat-start <starting latitude> --lon-start <starting longitude> --lat-end <ending latitude> --lon-end <ending longitude>
```

Here's an example with parameters filled in:

```
./manage.py query_cells --lat-start 39.7 --lon-start -89.7 --lat-end 38 --lon-end -88
```

It will query US Weather API for existing grid cells in the region.

By default, it will do 20 steps in each direction, resulting in up to 400 cells.

If you need more or less cells, change this value by adding `--steps <number of steps in each direction>` parameter.

Discovered grid cells will be stored in the database.

### Retrieving hourly forecasts for each cell 

This command will query hourly forecasts for each grid cell in the database:

```
./manage.py query_hourly_forecasts
```

Hourly forecasts will be stored in the database.

## Running API and web interface

You can start the web server with:

```
./manage.py runserver 8100
```

Open `http://127.0.0.1:8100/api` in your browser to access the web interface.

API documentation is available in the web interface.

## Tweaking settings

Override default settings in the `weather/settings.py` file, check `weather/settings.template` file for example.

Do not deploy in production with default settings.
