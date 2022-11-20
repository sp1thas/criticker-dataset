![criticker-dataset](https://www.criticker.com/img/sys/title_filmstv.png) **Dataset**

![build](https://github.com/sp1thas/criticker-dataset/workflows/build/badge.svg)
![python-version](https://img.shields.io/badge/Python-3.%5B8--10%5D-blue)
[![kaggle-dataset](https://img.shields.io/badge/KAGGLE_DATASET-20beff)](https://www.kaggle.com/sp1thas/criticker-dataset/) 
[![great_expectations](https://img.shields.io/badge/-great__expectations-white)](https://storage.googleapis.com/criticker-datadoc/index.html)

Yet another dataset about Movies, TV Shows and Games.

This is implementation of [Criticker Dataset](https://www.kaggle.com/sp1thas/criticker-dataset). This repository contains the necessesary spiders for dataset creation alongside with some basic tests.

`great_expectations` tool is used for Data Quality purposes, check here the [datadocs](https://storage.googleapis.com/criticker-datadoc/index.html)

`poetry` module is used for virtual environment and dependency management

## Install dependencies

```shell
poetry install
```

## Create dataset from scratch

```python
cd criticker
poetry run scrapy crawl games_spider -o games.csv # to retrieve games
poetry run scrapy crawl movies_spider -o movies.csv # to retrieve movies
```

## Development

### Run tests

```shell
poetry run python criticker/tests.py
```

## Next steps

 * [x] Add games
 * [ ] TCI related data
 * [ ] Add reviews


