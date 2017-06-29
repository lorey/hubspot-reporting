# Script to automate HubSpot Reporting

I love [HubSpot](https://hubspot.com) to organize my sales leads and to get an overview of my sales funnel. Because of that I use it for many projects and even for myself personally. In many situations, I need to get a quick overview of my funnel and/or send it to someone else, for example when writing reports for mentors or my startup's advisory board. That's why I created this script to generate diagrams of my sales funnel.

## So what can it do for you?

This Python script generates CSVs and diagrams for all of your sales pipelines automatically. This way, you can generate automated reports for your stakeholders, for example by including them in a LaTeX report.

## How does it work?

Running is as easy as

```
python3 main.py
```

The tool then executes to main tasks: It fetches the data, stores it in csv files and generates diagrams from the csv files afterwards. This way, you can extend the csv data if you like or separate the data generation from the plotting. Here's how the two steps work:

### 1: Fetch HubSpot data

In the first step, the tool fetches your pipelines via the HubSpot API. For each pipeline it generates a folder named like the the pipline_id (so don't worry if you see cryptic folders). The tool will then generate a CSV file named `data.csv` in each folder that looks like this:

```
date,deals_closed,deals_funnel,deals_amount_closed,deals_amount_funnel
2017-06-25 23:26:34.209553,10,11.8,0,0
2017-06-26 12:17:54.598448,10,11.9,0,0
2017-06-26 12:18:36.467397,10,11.9,0,0
2017-06-26 16:22:50.843669,10,12.3,0,0
2017-06-26 19:02:31.730476,11,13.0,0,0
2017-06-27 00:38:35.257576,11,13.0,0,0

```

For every run, one row is appended to the CSV file consisting of the following columns:

- date: The current `datetime` value.
- deals_closed: how many deals you have won.
- deals_funnel: how many deals you're expected to win, i.e. a deal with a percentage of 10% will count as 0.1 deals.
- deals_amount_closed: how much cash you've made with the won deals.
- deals_amount_funnel: how much cash you're expected to make, i.e. a deal with 50% win probability and an amount of 3000 will count as 50% * 3000 = 1500

### 2: Generate the plots from CSV

The second step generates the plots and saves png files in the according folders. For each pipeline, there are two plots:

- deal_amount.png: the monetary value of closed and expected deals
- deal_count.png: the number of closed and expected deals

The title of each diagram will contain the name of the pipeline. You can find the results in the `out` directory. The directory structure below shows the files inside the out directory:

```
├── config.py
├── hubspot
│   ├── api.py
│   ├── deals.py
│   └── __init__.py
├── main.py
├── out
│   ├── 666703db-8e54-49c1-be53-redacted
│   │   ├── data.csv
│   │   ├── deal_amount.png
│   │   └── deal_count.png
│   ├── 66659266-9d3f-41f3-8856-redacted
│   │   ├── data.csv
│   │   ├── deal_amount.png
│   │   └── deal_count.png
│   ├── default
│   │   ├── data.csv
│   │   ├── deal_amount.png
│   │   └── deal_count.png
│   ├── 666864eb-d814-4b5b-bfa1-redacted
│   │   ├── data.csv
│   │   ├── deal_amount.png
│   │   └── deal_count.png
│   └── overall
│       ├── data.csv
│       ├── deal_amount.png
│       └── deal_count.png
└── README.md
```

# Installation

The installation is pretty straightforward. Make sure matplotlib and requests are installed, create a config file as shown below, and run main.py periodically, for example by creating a cron job.

## config.py
You can generate an API key by clicking at your profile picture, then at `Integrations`, and finally at `HubSpot API key`

```
HUBSPOT_HAPIKEY = 'yourkeyhere'
```

# Also check my other HubSpot-related projects

- [Totally not Jarvis, a personal assisstant bot with HubSpot integration](https://github.com/lorey/totally-not-jarvis)
- [hubspot-contact-import: A HubSpot import tool for vcards and Xing](https://github.com/lorey/hubspot-contact-import)
- [hubspot-reporting: tool to generate diagrams from your hubspot data](https://github.com/lorey/hubspot-reporting)