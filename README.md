# Data Pipeline Project - Scraping Reddit r/new

```mermaid
%%{init: {'theme': 'dark', "flowchart" : { "curve" : "basis" } } }%%
graph TD
    subgraph Docker Compose
    subgraph Webscraper container
    B{Scraper} --> |get data as json|C[Pandas]
    Z[Pytest] --> |run tests|B
    end
    subgraph Shared Volume
    C --> |Save post content|E[CSV]
    C --> |Data quality statistics|D[(SQLite Logs)]
    end
    subgraph Streamlit Container
    P[Streamlit]
    E --> P
    end
    end
    
```

## Project Structure:

- Scrape reddit/r/new posts programatically, simulating "batch" data ingestion

- Parse scraped nested json data

- Clean excess metadata

- Use pytest for testing

- Track Data Quality Metrics

- Store metrics in SQLite database

- Write chunks of data to a csv

- Clean the CSV data

- Use Docker/Docker Compose for modularity

- Use containerized streamlit app for a dashboard/displaying outputs

## How to Run:

1. Clone the Repository

2. Run the docker commands in the root directory (which contains the docker compose file):

`docker compose build`

`docker compose up`

3. To open the streamlit app, open the Network Url output in the terminal in a browser.

4. After it finishes running, to remove the container:

`docker compose down --volumes`

5. After running, to clean up containers/volumes (assuming you don't have others on your system you need to save):

`docker system prune -a`

##### Note: If you refresh the streamlit app with "Ctrl + R", it will update the data to the lastest scraped while the scraper is continuously running.

## Alternate options to run it:

1. In the `app` directory, there are instructions to run the scraping portion of the app without using **docker compose**. It can be ran either locally (with a virtual env) or as a single docker container. 