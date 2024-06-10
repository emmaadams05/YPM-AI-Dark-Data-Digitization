from google.cloud import storage
import os

#set the project to be copesbrain
os.environ["GCLOUD_PROJECT"] = "copesbrain"

def list_blobs(bucket_name):
    """returns a dictionary of all file names in GCS bucket and their respective URIs"""

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    uri_dict = dict()

    #loop through all blobs
    for blob in blobs:
        #create a new dictionary entry to have the file name and respective URI
        uri_dict[blob.name]=("gs://" + blob.id[:-(len(str(blob.generation)) + 1)])

    return uri_dict

print(list_blobs("copesbrain_samplebucket1"))