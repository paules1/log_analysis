# Log Analysis Project

The project consist on creating a _python_ program which will be used to get and render the results of the analysis of a news web site log. The size of the log table is around 1.6 million records. 

#### Installation

If you are using MacOS or Windows, you can use <a href="https://www.vagrantup.com/downloads.html">Vagrant</a>
and <a href="https://www.virtualbox.org/">Virtual Box</a> to setup a local Linux environment.
Follow the instructions according to your operating system and complete Vagrant and Virtual Box installations.
    
Open a terminal or command prompt window in you computer and move to the folder on which you'll
be setting up the linux virtual box. Then execute these 3 commands:
 ```
$ vagrant init bento/ubuntu-16.04
$ vagrant up
$ vagrant ssh
```
Once you run the last command you'll be at the command prompt of your virtual linux box.
Execute the following commands to install the required components:
```
$ sudo apt-get update
$ sudo apt-get install zip unzip git postgresql
$ sudo apt-get -y install python-pip
$ pip install psycopg2
```
To setup the database content, use the following commands:
```
$ sudo su postgres -c 'createuser -dRS vagrant'
$ sudo su vagrant -c 'createdb news'
$ wget https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
$ unzip newsdata.zip
$ psql -d news -a -f newsdata.sql
```
Finally, get the code and complete the installation using this commands:

```
$ git clone https://github.com/paules1/log_analysis.git
$ cd log_analysis
$ git remote rm origin
$ psql -d news -a -f view.sql
```

_Running the program_ :  

```
$ python database.py
```
**Description**

The program first renders a menu of options for the user. By selecting the option, the program will execute a query on the db and renders the results.

**Files**
* database.py - Main script
* view.sql - Sql script to create a view on the database
* output.txt - Plain text file containing a copy of what the program prints out.



**Database Updates**

A new view was created on the database. The view produces a result set with 2 columns representing the number of views by article:

* article_slug
* counter

The _article_slug_ field is used as unique article identifier for joins.
```
CREATE VIEW view_articles_stats as
  SELECT
    REGEXP_REPLACE(path,'/article/','') as article_slug,
    COUNT(*) as counter
  FROM log
  WHERE status='200 OK'
  AND path!='/'
  GROUP BY path
  ORDER BY counter desc
```

**Project Status**
```
Submitted
```