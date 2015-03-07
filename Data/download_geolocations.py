import urllib
import zipfile,os.path
import os.path
import city_location_import

# Thanks to:
# http://stackoverflow.com/questions/19602931/basic-http-file-downloading-and-saving-to-disk-in-python
def download_geolocation(local_file_path):
    url = "http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity-latest.zip"
    print "Downloading geolocations file..."
    f = open(local_file_path,'wb')
    f.write(urllib.urlopen(url).read())
    f.close()
    print "Done downloading geolocations file"


# Thanks to:
# http://stackoverflow.com/questions/12886768/how-to-unzip-file-in-python-on-all-oses
def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
                zf.extract(member, path)


# Downloads the geolocation file if it does not exist
def download():
    if file_exists(city_location_import.file_path):
        print "File already downloaded, no need to download."
        return

    local_file_path = "/srv/departuretimes/Data/data/GeoLiteCity-Location.zip"
    local_file_path_unzipped = "/srv/departuretimes/Data/data/"  # 
    download_geolocation(local_file_path)
    unzip(local_file_path, local_file_path_unzipped)


def file_exists(fname):
    return os.path.isfile(fname) 

if __name__ == "__main__":
    download()
