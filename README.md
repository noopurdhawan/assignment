# Problem Statement
To create Web Service that provides basic analytics over taxi data. 
The live data can be obtained from BigQuery at Chicago Taxi trips. 
We will use only the following tables:
● bigquery-public-data.chicago_taxi_trips.taxi_trips

Creating Service on Google Cloud Enviornment for BigQuery: 
1. Navigate to browser tab, and Open Google cloud `https://console.cloud.google.com/`
2. Login by entering your credentials
3. On the left Panel, Click Google Cloud Platform go to IAM & admin and then Service Account.
4. Create New Service Account by clicking `CLick Service Account`.
    Fill in the details Service account name and description and hit create. 
5. Select Role from DropDown `BigQuery` and under that select  `BigQueryUser`
6. After this, set the Service account users role by putting your <email_id> and create Key.
7. Download the json file to the local System.

Setting up the local Env to run the application:
1. Install the python and pip 
2. Clone the project from github by git clone <project path>
3. To set the key for GCP for Bigquery.Open `user_config.ini` 
4. Set filename to path of the Downloaded Json Key file.

Run `sh install.sh` which would set the localhost on port 8080. 
Please make sure that port 8080 is not in use.





   
