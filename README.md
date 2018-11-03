# Log Analysis Project

The project consist on creating a _python_ program which will be used to get and render the results of the analysis of a news web site log. The size of the log table is around 1.6 million records. 

_Running the program_ :
```
python database.py
```
**Description**

The program first renders a menu of options for the user. By selecting the option, the program will execute a query on the db and renders the results.

**Files**
* database.py - Main script
* output.txt - Plain text file containing a copy of what the program prints out.



**Database Updates**

A new view was created on the database. The view produces a result set with 2 columns representing the number of views by article:

* article_slug
* counter

The _article_slug_ field is used as unique article identifier for joins.
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

**Project Status**
```
Submitted
```