#!/bin/env python3
import ajemdibi_process_utility as iii
from time import sleep
from random import randint
from config import db_host, db_database, db_user, db_password
from sqlalchemy import create_engine, text

################################################################################

movie_country = {}

iii.f_print('--------')
iii.f_print('Country process started')
engine = create_engine('mysql+mysqldb://' + db_user + ':' + db_password + '@' + db_host + '/' + db_database , echo = False)
conn = engine.connect()
trans = conn.begin()
sql = "select `id` from `tb_movie` where `genre` like '%Comedy%' and `rating` > 8 and `country` = '' order by `rating` desc, `title_primary_ascii` limit 19;"
result = conn.execute(text(sql))
trans.commit()
conn.close()

for row in result:
    # print(row)
    # print(row[0])
    sleep(randint(16, 46))
    movie_country[row[0]] = iii.f_get_country(row[0])
print(movie_country)

stmt = text("update `tb_movie` set `country` = :cc where `id` = :ii;")

iii.f_print('--------')

conn = engine.connect()
trans = conn.begin()
for id, country in movie_country.items():
    conn.execute(stmt, cc = country, ii = id)
trans.commit()
conn.close()


iii.f_print('Country process finished')
iii.f_print('--------')
################################################################################


# cc = 'tt1289403'
# print(cc + ': ' + iii.f_get_country(cc))
# cc = 'tt1289404'

