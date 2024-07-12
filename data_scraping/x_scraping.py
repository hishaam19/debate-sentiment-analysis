from apify_client import ApifyClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pytz
import json
import boto3

load_dotenv()

api_token= os.getenv('APIFY_API_TOKEN')

# Initialize the ApifyClient with your API token
client = ApifyClient(api_token)

# Initialize a session using AWS S3
s3 = boto3.client('s3')
bucket_name = 'x-sentiment-input'

def upload_to_s3(data, key):
    """Uploads data to S3 bucket.
    
    Keyword arguments:
    :param data: -- Data to be uploaded (JSON)
    :param key: -- S3 object key.
     """
    s3.put_object(Body=json.dumps(data), Bucket=bucket_name, Key=key)

# Calculate the start and end times for the 24-hour period before the current UTC time for scheduled run
# utc_now = datetime.now(pytz.utc)
# start_time = (utc_now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
# end_time = utc_now.strftime("%Y-%m-%dT%H:%M:%SZ")

# Start time for the presidential debate plus 24 hour period to grab X posts from
start_time = datetime(2023, 6, 27, 21, 0, 0, tzinfo=pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
end_time = datetime(2023, 6, 28, 20, 59, 0, tzinfo=pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Prepare the Actor input
run_input = {
    "startUrls": [
        "https://twitter.com/search?q=(Trump%20OR%20Biden)%20AND%20(Ukraine%20OR%20Israel)&src=typed_query",
        "https://twitter.com/search?q=%23TrumpUkraine%20OR%20%23BidenIsrael&src=typed_query",
    ],
    "searchTerms": [
        "\"Donald Trump\" AND Ukraine",
        "\"Donald Trump\" AND Israel",
        "\"Joe Biden\" AND Ukraine",
        "\"Joe Biden\" AND Israel",
        "Trump Ukraine",
        "Trump Israel",
        "Biden Ukraine",
        "Biden Israel",
        "#TrumpUkraine",
        "#TrumpIsrael",
        "#BidenUkraine",
        "#BidenIsrael",
        "#Debate2024",
    ],
    "maxItems": 16000,
    "sort": "Latest",
    "tweetLanguage": "en",
    "start": start_time,
    "end": end_time,
}

# Run the Actor and wait for it to finish
run = client.actor("61RPP7dywgiy0JPD0").call(run_input=run_input)

# Fetch items from the actor's dataset and upload to S3
for i, item in enumerate(client.dataset(run["defaultDatasetId"]).iterate_items()):
    upload_to_s3(item, f'raw/item_{i}.json')
