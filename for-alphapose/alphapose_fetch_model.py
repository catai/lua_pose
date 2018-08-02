import os
import zipfile
#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039#taken
import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

os.chdir('./human-detection')
file_id = '1dMiUPMvt5o-S1BjDkzUJooEoT3GgasxB'
destination = './output.zip'

if not os.path.isdir('./output'):
    download_file_from_google_drive(file_id, destination)
    with zipfile.ZipFile(destination,"r") as zip_ref:
        zip_ref.extractall("./")
    os.remove(destination)
os.chdir('../predict')
os.mkdir('models')
os.chdir('models')

file_id = '1JYlLspGJHJFIggkDll4MdUdqX2ELqHpk'
destination='./final_model.t7'
if not os.path.isfile(destination):
    download_file_from_google_drive(file_id, destination)
os.chdir('../..')
