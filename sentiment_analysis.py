import json
import boto3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def tag_tweet(text):
    tags = []
    text = text.lower()  
    if "biden" in text:
        if "ukraine" in text:
            tags.append("Biden-Ukraine")
        if "israel" in text:
            tags.append("Biden-Israel")
    if "trump" in text:
        if "ukraine" in text:
            tags.append("Trump-Ukraine")
        if "israel" in text:
            tags.append("Trump-Israel")
    return tags

def analyze_and_save_sentiment(s3_client, input_bucket, output_bucket, key, index):
    obj = s3_client.get_object(Bucket=input_bucket, Key=key)
    tweet_data = obj['Body'].read().decode('utf-8')  
    tweet = json.loads(tweet_data)
    text = tweet['text'] if 'text' in tweet else '' 

    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(text)
    sentiment = {
        'tweet': text,
        'sentiment_score': vs['compound'],
        'positive': vs['pos'],
        'negative': vs['neg'],
        'neutral': vs['neu'],
        'tags': tag_tweet(text)
    }

    # Upload the sentiment result to S3
    result_key = f'processed/sentiment_result_{index}.json'
    s3_client.put_object(Bucket=output_bucket, Key=result_key, Body=json.dumps(sentiment))

def process_tweets(input_bucket, output_bucket, prefix='raw/'):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=input_bucket, Prefix=prefix)

    if 'Contents' in response:
        for index, obj in enumerate(response['Contents']):
            key = obj['Key']
            if key.endswith('.json'):
                analyze_and_save_sentiment(s3_client, input_bucket, output_bucket, key, index)

input_bucket = 'x-sentiment-input'
output_bucket = 'x-sentiment-output'
process_tweets(input_bucket, output_bucket)
