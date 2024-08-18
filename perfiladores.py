import requests
import json
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.colab import files
import numpy as np

gs_cred = {
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}

with open('gs_cred.json','w') as outfile:
  json.dump(gs_cred,outfile)

#RETRIEVE FOLDERS ASSIGNED TO A SPECIFIC OWNER
url = 'https://expedientes.mx/expedienteazul/api/folder/active-folders?owner_id=57'

headers = {'customer_id':'140','token_key':'YOUR_TOKEN'}
response = requests.request('POST',url,data=headers)

r1 = json.loads(response.text.encode('utf8'))
folders = pd.DataFrame(r1)

#RETRIEVE FILES UPLOADED TO THE FOLDERS
column_names = ["name","document_id", "status", "comments", "valid_until", "files", "form_values","folder_id"]
files = pd.DataFrame(columns = column_names)
empty = []

for x in folders['folder_id']:
  url = 'https://expedientes.mx/expedienteazul/api/folder/folder-documents?folder_id='+str(x)

  headers = {'customer_id':'140','token_key':'Y0UR_TOKEN'}
  response = requests.request('POST',url,data=headers)
  r1 = json.loads(response.text.encode('utf8'))
  data1 = pd.DataFrame(r1)
  data1["folder_id"]=x
  files = pd.concat([files, data1], ignore_index=True)

files.fillna('', inplace=True)
files['files'] = files['files'].apply(lambda y: np.nan if len(y)==0 else y)
files['form_values'] = files['form_values'].apply(lambda y: np.nan if len(y)==0 else y)
files1 = files.dropna(axis = 0, subset=['files'])
files2 = files1[['name','document_id','folder_id','status']]
files3 = files[['folder_id','document_id','status','name']]

#INSERT FOLDERS DATAFRAME INTO A GOOGLE SHEETS
file = r'gs_cred.json'
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(file, scope)
client = gspread.authorize(creds)

gs_book='YOUR_BOOK'
gs_url = 'https://docs.google.com/spreadsheets/d/'+gs_book+'/edit'
gs_sheet = 'folders'

sheet = client.open_by_url(gs_url).worksheet(gs_sheet)
sheet.clear()
sheet.insert_rows([folders.columns.values.tolist()],row=1, value_input_option='RAW')
sheet.insert_rows(folders.values.tolist(),row=2, value_input_option='RAW')

#INSERT FILES DATAFRAME INTO A GOOGLE SHEETS
gs_book='YOUR_BOOK'
gs_url = 'https://docs.google.com/spreadsheets/d/'+gs_book+'/edit'
gs_sheet = 'files'

sheet = client.open_by_url(gs_url).worksheet(gs_sheet)
sheet.clear()
sheet.insert_rows([files3.columns.values.tolist()],row=1, value_input_option='RAW')
sheet.insert_rows(files3.values.tolist(),row=2, value_input_option='RAW')

