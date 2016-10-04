#!/usr/bin/env python
import os, re, sys
import requests
from pipes import quote
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from sh import unzip
import shutil


def convert_to_geojson(path):
    """
    Receive a path to zip file.
    Unzip the file, convert .shp files within to GeoJSON data files.
    Return a list of paths to the GeoJSON files.
    """
    outdir = path.rstrip('.zip')
    basename = outdir.split('/')[-1]

    if os.path.exists(outdir): # Delete any existing outdir
        shutil.rmtree(outdir)
    os.makedirs(outdir, exist_ok=True)
    unzip(path, '-d', outdir)

    geojson_files = []

    for filename in os.listdir(outdir):
        if filename.endswith(".shp"):
            shpFile = os.path.join(outdir, filename)
            geojsonFile = shpFile.replace('.shp', '.geojson')
            print(shpFile, geojsonFile)

            ogr_command = 'ogr2ogr -f "GeoJSON" -t_srs crs:84 {outpath} {inpath}'.format(outpath=quote(geojsonFile), inpath=quote(shpFile))

            os.popen(ogr_command).read()
            geojson_files.append(geojsonFile)

    return geojson_files


def download(url, to):
    """
    Receive a URL and download it as a ZIP,
    adding the .zip extension because
    Long Beach GIS data files are served without extension
    """
    filename = url.rstrip('/').split('/')[-1] + '.zip'
    r = requests.get(url, stream=True)

    outpath = os.path.join(to, filename)

    with open(outpath, 'wb') as fd:
        for chunk in r.iter_content(1024 * 1024):
            fd.write(chunk)

    return outpath


def scrape_gis_data_catalog():
    result = requests.get(base_url)
    soup = BeautifulSoup(result.content, 'html.parser')

    rows = soup.find('table').findAll(lambda tag: tag.name=='tr')

    for this_row in rows[2:]:
        cells = this_row.findAll('td')

        # title_data = cells[0].string
        # titleMatchObj = re.match( r'(.*) \(posted (.*?)\)', title_data)
        # title = titleMatchObj.group(1)
        # date = titleMatchObj.group(2)

        url = urljoin(base_url, cells[2].find('a').get('href'))
        zipfile = download(url, tmp_path)
        for file in convert_to_geojson(zipfile):
            shutil.move(file, os.path.join(repo_path, os.path.basename(file)))


if __name__ == "__main__":
    base_url = 'http://www.longbeach.gov/ti/gis-maps-and-data/data-catalog/'
    repo_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    tmp_path = os.path.join(repo_path, 'tmp')
    os.makedirs(tmp_path, exist_ok=True)

    scrape_gis_data_catalog()