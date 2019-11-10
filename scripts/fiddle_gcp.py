from google.cloud import storage
from os import listdir
from os.path import isfile, join

bucket_name = "travis_recommender"
bucket_folder = "csv_data\\"  # doesn't work cos gcp is unix
bucket_folder = "csv_data/"  # the correct way for unix
file_name = "locations_recommender.csv"
credentials="" # inesrt Gmaps api key here
project = "travis-test-01"
json_keyfile = 'Travis-test-01-35fea3db5a86.json'
storage_client = storage.Client.from_service_account_json(json_keyfile)

bucket = storage_client.get_bucket(bucket_name)  # now it will create bucket obj

local_folder = "travis_optimiser\\test_data\\"
def upload_files(bucket_name, bucket, local_folder):
    """Upload files to GCP bucket."""
    # files = [f for f in listdir(local_folder) if isfile(join(local_folder, f))]
    file = 'locations.csv'
    localFile = local_folder + file
    blob = bucket.blob(bucket_folder + file)
    blob.upload_from_filename(localFile)
    return f'Uploaded {file} to "{bucket_name}" bucket.'

upload_files(bucket_name, bucket, local_folder)

def list_files(bucket_name, bucket_folder):
    """List all files in GCP bucket."""
    files = bucket.list_blobs(prefix=bucket_folder)
    fileList = [file.name for file in files if '.' in file.name]
    return fileList

list_files(bucket_name, bucket_folder)

def download_file(bucket):
    bucket_folder = "csv_data/"  # the correct way for unix
    file = "locations_recommender.csv"
    blob = bucket.blob(bucket_folder + file)
    filename = blob.name.split('/')[-1]
    local_folder = "scripts"
    dl_path = join(local_folder, filename)
    blob.download_to_filename(dl_path)
    return f'{filename} downloaded from bucket.'

download_file(bucket)  # will download the csv to bucket

def delete_file(bucket_name, bucket_folder, filename):
    """Delete file from GCP bucket."""
    bucket.delete_blob(bucket_folder + filename)
    return f'{filename} deleted from bucket.'

