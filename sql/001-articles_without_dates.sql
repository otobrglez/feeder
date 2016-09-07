SELECT COUNT(*)
FROM
  (SELECT
     a.scraped_url,
     a.domain,
     a.scraped_at,
     date_at,
     title_raw
   FROM
     articles a
   WHERE
     -- a.scraped_url LIKE '%umrl%'
     a.date_at IS NOT NULL
   GROUP BY
     scraped_url,
     a.domain,
     scraped_at,
     date_at,
     title_raw
   ORDER BY
     a.scraped_at DESC) AS articles_sub

-- {http://m.delo.si/images/460/full/}