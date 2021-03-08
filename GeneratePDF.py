import msal
import requests
import json
import time
import sys


f = open('data.json',"r")
config = json.load(f)
f.close

# Tenant/Report specific configurations
TENANT_ID = config['tenant_id']
WORKSPACE_ID = config['workspace_id']
REPORT_ID = config['report_id']

# Service Principal Credentials
CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']

# Scopes defined for authentication
SCOPE = config['scope']
AUTHORITY = config['authority'].replace('organizations',TENANT_ID)

URL_EXPORT_TO_FILE = config['url_export_to_file'].replace('WORKSPACE_ID',WORKSPACE_ID).replace('REPORT_ID',REPORT_ID)
URL_EXPORT_FILE_PATH = config['url_export_file_path'].replace('WORKSPACE_ID',WORKSPACE_ID).replace('REPORT_ID',REPORT_ID)


def main():
    clientapp = msal.ConfidentialClientApplication(CLIENT_ID, CLIENT_SECRET, authority=AUTHORITY)
    
    response = clientapp.acquire_token_for_client(scopes=SCOPE)
    token = response['access_token']    
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    ### POST call to invoke Export To PDF option
    data = {}
    data['format'] = 'pdf'
    json_data = json.dumps(data)
    api_response = requests.post(URL_EXPORT_TO_FILE, headers=header, data=json_data)
    try:
        export_id = api_response.json()['id']
    except:
        print(api_response.content)
        return

    download_file_path = get_download_file_path(export_id, header)
    file_location = download_file(download_file_path, header)
    # print(file_location)

def get_download_file_path(export_id, header):
    file_status = 'Running'
    file_location = ''
    counter = 0
    while(file_status.lower() != 'succeeded' and counter++ < 100):
        ### GET call to get status of exportId
        url = URL_EXPORT_FILE_PATH + export_id
        try:
            api_response = requests.get(url, headers=header)
            resp = api_response.json()
            percent = resp['percentComplete']
            print(f'Percentage complete: {percent}')
            file_status = resp['status']
            time.sleep(3)
        except:
            print(api_response.content)
            return

    file_location = api_response.json()['resourceLocation']
    # print(f'The file can be downloaded from the URL: {file_location}')
    return file_location

def download_file(url, header):
    local_filename = url.split('/')[-1] + ".pdf"
    # NOTE the stream=True parameter below
    with requests.get(url, headers=header, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename


if __name__ == "__main__":
   main()
