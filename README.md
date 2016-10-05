# Welcome to HackLB/gis-data-catalog

This repository is intended to mirror the [OpenLB GIS datasets](http://www.longbeach.gov/ti/gis-maps-and-data/data-catalog/) using GeoJSON for convenience and readiness to integrate with many modern GIS technologies such as OpenStreetMaps, Leafly, Mapbox, and Github itself*

This project is an activity of [HackLB](https://github.com/HackLB).

## Viewing the GeoJSON datasets

Thanks to Github's [excellent GeoJSON support](https://help.github.com/articles/mapping-geojson-files-on-github/), you may view these GeoJSON datasets directly from your browser. Simply navigate to the GeoJSON document from Github's Web interface - for instance, by viewing this link: <https://github.com/HackLB/gis-data-catalog/blob/master/Bikeways.geojson>

## Using this repo

### Clone it and go

You may easily [clone](https://github.com/HackLB/gis-data-catalog.git) or [download](https://github.com/HackLB/gis-data-catalog/archive/master.zip) the contents of this library using any git client (including the Github Web interface) to begin incorporating the GeoJSON files into your projects. I'll do my best to keep this repository up to date with the latest datasets from the city.

### Maintaining your own mirror

If you'd rather download the city's original datasets and convert them yourself, I've included the same script `update.py` I wrote to maintain this repo. Here's what you need to know.

#### Requirements

1. `Python 3.5+` (it may work on Python 2.7 but I haven't tested it)
2. `GDAL` library - on OSX use homebrew to install: `brew install gdal`
3. `ogr2ogr` - should be part of GDAL
4. Several Python packages installed with pip, documented in `requirements.txt`

#### How to Use update.py

1. make a Python 3 virtualenv for this project
2. `pip install -r requirements.txt` to satisfy dependencies
3. `./update.py`

The script will create a `tmp` directory within the repo where it'll download the original datasets from the city and unzip them. Once it's done processing, the new GeoJSON files will be moved from `tmp` into the repos root directory, overwriting any existing datasets.

You may delete the `tmp` directory or its contents after running the script to save space.


### Contributing to this repo

Pull requests are welcome - if you have an idea for an improvement (for instance, porting `update.py` to another language) you're welcome to make it and open a PR, or open an issue first for discussion.