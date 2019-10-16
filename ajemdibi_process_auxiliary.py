#!/bin/env python3
import ajemdibi_process_utility as iii
from time import sleep
from random import randint
from config import db_host, db_database, db_user, db_password
from sqlalchemy import create_engine, text

################################################################################

movie_country = {}
movie_type = {}

iii.f_print('--------')
iii.f_print('Auxiliary process started')
iii.f_print('--------')

engine = create_engine('mysql+mysqldb://' + db_user + ':' + db_password + '@' + db_host + '/' + db_database , echo = False)
conn = engine.connect()
trans = conn.begin()
# sql = "select `id` from `tb_movie` where (`genre` like '%Comedy%' or `genre` like '%Romance%' ) and `rating` > 7.5 and `country` = '' order by `year` desc, `rating` desc, `title_primary_ascii` limit 19;"

sql = (" select `id` from `tb_movie`"
       " where `country` = ''"
       " order by `year` desc, `rating` desc, `title_primary_ascii`"
       " limit 19;") # use opening and closing brackets to concatenate multiple lines
result = conn.execute(text(sql))
trans.commit()
conn.close()

for row in result:
    sleep(randint(16, 46))
    content = iii.f_get_html_page(row[0])
    movie_country[row[0]] = iii.f_get_country(content)
    movie_type[row[0]] = iii.f_get_movie_type(content)
    iii.f_print('movie_country : ' + row[0] + ' : ' + movie_country[row[0]])
    iii.f_print('movie_type    : ' + row[0] + ' : ' + movie_type[row[0]])


engine = create_engine('mysql+mysqldb://' + db_user + ':' + db_password + '@' + db_host + '/' + db_database , echo = False)
conn = engine.connect()
trans = conn.begin()
stmt = text("update `tb_movie` set `country` = :cc where `id` = :ii;")
stmt_delete = text("delete from `tb_auxiliary` where `id` = :ii")
stmt_insert = text("insert into `tb_auxiliary`(`id`, `country`, `movie_type`) values (:ii, :cc, :mm)")

for id, country in movie_country.items():
    conn.execute(stmt, cc = country, ii = id)
    conn.execute(stmt_delete, ii = id)
    conn.execute(stmt_insert, ii = id, cc = country, mm = movie_type[id])
trans.commit()
conn.close()

iii.f_print('--------')
iii.f_print('Auxiliary process finished')
iii.f_print('--------')
################################################################################


