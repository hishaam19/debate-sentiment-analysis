# Debate Sentiment Analysis

## Overview
This project aims to analyze public sentiment concerning presidential candidates' stances on foreign policy, particularly focusing on their positions on Israel and Ukraine. The analysis pipeline extracts tweets, performs sentiment analysis, and visualizes the results to provide insights into public opinion.

## Components
The project integrates several technologies and services to manage data collection, storage, processing, and visualization.

### Data Collection
- **Apify Actor**: Utilizes Apify to scrape tweets based on specific keywords related to the presidential candidates and their foreign policy stances. The configuration allows for scraping data that directly correlates with public sentiments on Twitter.

### Data Storage
- **AWS S3**: Stores the raw tweet data and processed results in separate S3 buckets. The raw data is stored under `x-sentiment-input/raw/` with each tweet saved as an individual JSON file. Processed data is stored in `x-sentiment-output/processed/` after sentiment analysis.

### Data Processing
- **Python & VADER Sentiment Analysis**: Python scripts are used to load data from S3, perform sentiment analysis using the VADER library, and save the sentiment scores back to S3. This includes tagging each tweet with relevant topics for more granular analysis.

### Visualization
- **Power BI**: Connects to the processed data via Amazon Athena, which queries the S3 buckets to retrieve sentiment analysis results. Power BI dashboards provide visual insights into sentiment trends over time and categorize sentiments by topics and overall public perception.

## Architecture
The project's architecture involves:
- **AWS Services**: Utilizes Amazon S3 for data storage, AWS Glue for managing data cataloging, and Amazon Athena for querying processed data.
- **Power BI**: Uses Power BI for creating interactive dashboards that help in visualizing data insights and trends.

## Setup and Configuration
### AWS Configuration
- Ensure appropriate IAM roles and policies are in place for accessing S3 buckets and running Athena queries.
- Set up AWS Glue crawlers to catalog S3 data for querying.

### Power BI Setup
- Connect Power BI to Amazon Athena with the ODBC driver configured to access the AWS Glue Data Catalog.
- Design dashboards to reflect findings and update them periodically to include new analysis results.

### Running the Apify Actor
- Monitor Apify runs and handle any exceptions or errors during data collection.

## Usage
To run the sentiment analysis pipeline:
1. Trigger the Apify actor to collect data and store it in `x-sentiment-input`.
2. Execute Python scripts to process raw data and upload results to `x-sentiment-output`.
3. Use Power BI to visualize and analyze the processed data through Athena queries.
