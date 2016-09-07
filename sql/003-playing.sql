WITH raw_articles AS (SELECT
                        DISTINCT ON (articles.scraped_url) articles.*
                      FROM articles)

SELECT
  raw_articles.mobile_source_url
FROM raw_articles
ORDER BY date_at DESC

-- SELECT COUNT(DISTINCT articles.scraped_url) FROM articles;