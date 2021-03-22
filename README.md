# Problem Statement
To create Web Service that provides basic analytics over taxi data. 
The live data can be obtained from BigQuery at Chicago Taxi trips. 
We will use only the following tables:`bigquery-public-data.chicago_taxi_trips.taxi_trips`

1. Set up the Google Cloud Project by steps, 
    https://developers.google.com/workspace/marketplace/create-gcp-project
    
2. Installing Google Cloud SDK by following steps,
    https://cloud.google.com/sdk/docs/install
    
3. Creating Service on Google Cloud Enviornment for BigQuery: 
    1. Navigate to browser tab, and Open Google cloud `https://console.cloud.google.com/`
    2. Login by entering your credentials
    3. On the left Panel, Click Google Cloud Platform go to IAM & admin and then `Service Accounts`.
    4. Create New Service Account by clicking `CLick Service Account`.
        Fill in the details Service account name and description and hit create. 
    5. Select Role from DropDown `BigQuery` and under that select  `BigQueryUser`
    6. After this, set the Service account users role by setting your <email_id> 
    7. For Create Key. Goto Google Project Service and select the service created .
    8. Under tab `Keys` add keys and download it in json format to the local System.

4. Setting up the local Env to run the application:
    1. Clone the project from github by git clone <project path>
    2. To set the key for GCP for Bigquery.Open `user_config.ini` 
    3. Set filename to path of the Downloaded Json Key file.

5. Run `sh install.sh` which would set the localhost on port 8080. 
   Please make sure that port 8080 is not in use.





   
