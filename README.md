# Log Analysis Project

The project consist on creating a _python_ script which will be used to obtain and render the results of the log analysis of a news web site. The output represents statistics for favorite articles, favorites authors, and days on which a significant number of errors occurred while processing web requests. The size of the log is around 1.6 million requests.   

### Views
To speed up the performance of 2 of the project queries, a new view was created on the database. The view produces a result set with 2 columns representing the number of views by article:

* article_slug
* counter

The _article_slug_ field will be used as the _reference key_ to relate the numbers to articles.
```
create view view_articles_stats as
select
  regexp_replace(path,'/article/','') as article_slug,
  count(*) as counter
from log
  where status='200 OK'
  and path!='/'
group by path
order by counter desc
```

#### Code Status
```
Under review.
```