#!/usr/bin/env python3

import psycopg2
import datetime

DB_NAME = 'news'

CHOICE_TEXTS = [
    '',
    '[1] What are the most popular three articles of all time?',
    '[2] Who are the most popular article authors of all time?',
    '[3] On which days did more than 1% of requests lead to errors?',
    '[q] Enter q to quit'
]


def output_to_screen(choice_number, rows, row_template):
    print('{t:^}'.format(t=CHOICE_TEXTS[choice_number]))
    print("\n")
    rec = 0
    for row in rows:
        rec += 1
        print(row_template.format(rec=rec, data=row))
    print("\n")


def execute_query(query):
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def popular_articles():
    query = '''select
            articles.id,
            articles.title,
            stats.counter
            from view_articles_stats as stats
            left join articles on articles.slug = stats.article_slug;'''
    return execute_query(query)


def popular_authors():
    query = '''select
            authors.id,
            authors.name,
            sum(stats.counter) as counter
            from view_articles_stats as stats
            left join articles on articles.slug = stats.article_slug
            left join authors on articles.author = authors.id
            group by authors.id, authors.name
            order by counter desc;'''
    return execute_query(query)


def error_stats():
    query = '''select
            date(time) as time,
            count(case when status!='200 OK' then 1 end) as count_error,
            count(*) as counter ,
            ROUND(CAST(count(case when status!='200 OK' then 1 end)/count(*)::float*100 as numeric),2) as percent
            from log
            group by date(time)
            having count(case when status!='200 OK' then 1 end)/count(*)::float>0.01;'''
    return execute_query(query)


if __name__ == '__main__':
    choice = ''
    while choice != 'q':
        print("\n")
        print(" {text}".format(text=CHOICE_TEXTS[1]))
        print(' {text}'.format(text=CHOICE_TEXTS[2]))
        print(' {text}'.format(text=CHOICE_TEXTS[3]))
        print(' {text}'.format(text=CHOICE_TEXTS[4]))
        print("\n")
        choice = raw_input('What would you like to view? ')
        print("\n")
        if choice == '1':
            output_to_screen(
                1,
                popular_articles(),
                ' {rec:<2} | {data[2]:>8} views | {data[1]:<20}'
            )
        elif choice == '2':
            output_to_screen(
                2,
                popular_authors(),
                ' {rec:<2} | {data[2]:>8} views | {data[1]:<20}',
            )
        elif choice == '3':
            output_to_screen(
                3,
                error_stats(),
                ' {data[0]} | {data[3]}%',
            )
        elif choice == 'q':
            print("\nSee you later.\n")
        else:
            print("\nI don't understand your choice, please try again.\n")