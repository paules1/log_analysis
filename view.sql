-- Creating the view

CREATE VIEW view_articles_stats as
  SELECT
    REGEXP_REPLACE(path,'/article/','') as article_slug,
    COUNT(*) as counter
  FROM log
  WHERE status='200 OK'
  AND path!='/'
  GROUP BY path
  ORDER BY counter desc;