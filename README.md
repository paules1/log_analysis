# Log Analysis Project

The project consist on creating a _python_ program which will be used to get and render the results of the analysis of a news web site log. The program first renders a menu of options for the user:
* Favorite articles
* Favorite authors
* Days on which a significant number of errors occurred while processing web requests.

The size of the log table is around 1.6 million records.   

### Files
* database.py - Main script
* output.txt - Plain text file containing a copy of what your program prints out.



### Database
A new view was created on the database. The view produces a result set with 2 columns representing the number of views by article:

* article_slug
* counter

The _article_slug_ field is used as unique identifier of the article and used as the _reference key_ to join with articles table.
```
create view
view_articles_stats as
  select
    regexp_replace(path,'/article/','') as article_slug,
    count(*) as counter
  from log
    where status='200 OK'
    and path!='/'
  group by path
  order by counter desc
```

#### Project Status
```
Submitted.
```