## Web scraping tool
- Built using python fastapi and beautifulsoup4.
- Configurable storage support
  - local or configurable db string.
- Response caching support using redis.
- Notifying scraping status with console or api
- Using inbuilt simple fast api authentication.

### Endpoints
1. Fetch page: GET
- http://127.0.0.1:8000/events/page/<page-no>
- Authorization: Basic auth (user/password)

2. Fetch page ranges : POST
- Request body: 
  - {
    "from_page":"2",
    "to_page":"2"
    }
- http://127.0.0.1:8000/events/range
- Authorization: Basic auth (user/password)

3. No. of items scraped: GET
- http://127.0.0.1:8000/scrape_count 

### Info
- Configurations are stored in src/config.properties file.
- storage options - local/db.
- caching support by redis - find in docker-compose.yml file.
- results - query results & images are stored locally if local storagting is enabled. (images - src/res and results in src/ folder)


### Installation
```sh
pip install -r requirements.txt
```

