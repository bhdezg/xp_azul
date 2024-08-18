# xp_azul

## Introduction
This Python script retrieves folder and file data from a the Expediente Azul API and store this data into Google Sheets. It performs the following tasks:
1. Retrieves Folders: Fetches folders assigned to a specific owner using a provided API endpoint.
2. Retrieves Files: Extracts file details from these folders.
3. Cleans Data: Processes and cleans the retrieved data.
4.Uploads Data: Inserts the cleaned data into Google Sheets.

##Setup
Google Sheets Credentials:

Obtain a [service account key file](https://developers.google.com/workspace/guides/create-credentials?hl=en) from the Google Cloud Console.
Save the key file as gs_cred.json.

Update Script:
Replace YOUR_TOKEN with your actual API token.
Replace YOUR_BOOK with your Google Sheets document ID.
Update the gs_cred dictionary with your Google service account credentials.


## Requirements

1. Python 3.x installed on your system.
2. A compatible SQL database system (e.g., MySQL).
3. An account in https://xpazul.com/financiera/
