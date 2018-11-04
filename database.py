#!/usr/bin/env python3

import psycopg2

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
    query = '''
        SELECT
            articles.id,
            articles.title,
            stats.counter
        FROM view_articles_stats as stats
        LEFT JOIN articles on articles.slug = stats.article_slug;'''
    return execute_query(query)


def popular_authors():
    query = '''
        SELECT
            authors.id,
            authors.name,
            SUM(stats.counter) as counter
        FROM view_articles_stats as stats
        LEFT JOIN articles on articles.slug = stats.article_slug
        LEFT JOIN authors on articles.author = authors.id
        GROUP BY authors.id, authors.name
        ORDER BY counter desc;'''
    return execute_query(query)


def error_stats():
    query = '''
        SELECT
            DATE(time) as time,
            COUNT(case when status!='200 OK' then 1 end) as count_error,
            COUNT(*) as counter ,
            ROUND(
                COUNT(case when status!='200 OK' then 1 end)/(COUNT(*)*1.0)*100
                ,2
            ) as percent
        FROM log
        GROUP BY DATE(time)
        HAVING
              COUNT(case when status!='200 OK' then 1 end)
              /(COUNT(*)*1.0)>0.01;'''
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
