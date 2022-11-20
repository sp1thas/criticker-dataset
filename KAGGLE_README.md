# Criticker Dataset

Yet another dataset about movies. This dataset consists of more than 100K movies/TV shows items. Data are scraped from [criticker.com]() and for each item meta-data fields like title, description, and publish date are provided. Below you will find an extensive description for each field.

**What makes this dataset different:**

 * [x] **Then is comes to deep learning, size does matter**. My goal is to create a huge dataset with almost every movie/tv show item from criticker.
 * [ ] **Ratings and Reviews**.

`great_expectations` tool is used for Data Quality purposes, check here the [datadocs](https://storage.googleapis.com/criticker-datadoc/index.html)

## Content

`movies.csv` contains almost every movie/tv show from criticker. For each item the following fields are available (wherever is applicable):


| field name     | description                                                                                     | field type |
|----------------|-------------------------------------------------------------------------------------------------|------------|
| actors         | Comma-separated actors' names                                                                   | str        |
| akas           | Comma-separated AKA (As Known as) names                                                         | str        |
| avg_percentile | Ratings average percentile                                                                      | float      |
| counties       | Comma-separated countries                                                                       | str        |
| creators       | Comma-separated creators' names                                                                 | str        |
| date_published | \[For films only\] Year of publish                                                              | int        |
| description    | Description                                                                                     | str        |
| directors      | Comma-separated directors' names                                                                | str        |
| end_date       | \[For TV Shows only\] End year                                                                  | int        |
| franchises     | Comma-separated franchises                                                                      | str        |
| genres         | Comma-separated genres                                                                          | str        |
| n_ratings      | Total number of ratings                                                                         | int        |
| name           | Name                                                                                            | str        |
| poster_url     | Poster's url                                                                                    | str        |
| rss_feed_url   | RSS Feed url                                                                                    | str        |
| start_date     | \[For TV Shows only\] Start year                                                                | int        |
| trailer_url    | Youtube trailer url                                                                             | str        |
| type           | Type like Short Film, TV Show and others. Empty type means that item is probably a regular film | str        |
| uid            | md5 Unique ID                                                                                   | str        |
| url            | URL                                                                                             | str        |
| writers        | Comma-separated writers' names                                                                  | str        | 

## Next Steps

 * [ ] Add ratings and reviews
  