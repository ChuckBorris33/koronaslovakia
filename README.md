# Korona stats

Small application for scrapping and displaying statistics about corona virus cases in Slovakia. Data is scrapped from official government site www.korona.gov.sk

App is running at [www.korona.zalman.online](www.korona.zalman.online)


## Development

### Backend

#### Install dependencies

```bash
poetry install
```

#### Setup database

You can download database from https://korona.zalman.online/database.sqlite.
```bash
# From repo root directory
curl https://korona.zalman.online/database --output app.db
```

Or setup fresh database
```bash
poetry run flask migrate
```


#### Run development server

```bash
poetry run flask run
```

#### Code checks

```bash
poetry shell
black .
mypy .
flake8
pytest
```

### Frontend

#### Install dependencies

```bash
yarn install
```

#### Run development server

```bash
yarn dev
```

#### Code formatting

```bash
yarn format
```



