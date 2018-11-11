#!/bin/env python3
import ajemdibi_process_utility as iii
import shutil
import urllib.request
import os
from config import db_host, db_database, db_user, db_password
from sqlalchemy import create_engine, text


directory    = os.path.expanduser('~') + '/ajemdibi/'

file_movies  = 'ajemdibi_movies_tsv.gz'
file_ratings = 'ajemdibi_ratings_tsv.gz'
file_sql_out = 'ajemdibi_movies_final_out.sql'

url_movies   = 'https://datasets.imdbws.com/title.basics.tsv.gz'
url_ratings  = 'https://datasets.imdbws.com/title.ratings.tsv.gz'

list_movies_out  = []
list_ratings_out = []

dict_movies      = {}
dict_ratings     = {}
dict_out         = {}


################################################################################
iii.f_print('--------')
iii.f_print('Movies file download started')
#f = open(file_name, 'bw')
with urllib.request.urlopen(url_movies) as response, open(directory + file_movies, 'wb') as f:
    shutil.copyfileobj(response, f)
#f.close()
iii.f_print('Movies file download finished')
################################################################################
iii.f_print('---------')
iii.f_print('Ratings file download started')
with urllib.request.urlopen(url_ratings) as response, open(directory + file_ratings, 'wb') as f:
    shutil.copyfileobj(response, f)
iii.f_print('Ratings file download finished')
################################################################################
iii.f_print('---------')
iii.f_print('Ratings file read started')
list_ratings = iii.f_read_gzip_file(directory + file_ratings)
iii.f_print('Ratings file read finished')
################################################################################
iii.f_print('--------')
iii.f_print('Movies file read started')
list_movies = iii.f_read_gzip_file(directory + file_movies)
iii.f_print('Movies file read finished')
################################################################################
iii.f_print('--------')
iii.f_print('Ratings process started')

for i, line in enumerate(list_ratings):
    movie_id, rating, vote = '','',''
    movie_id, rating, vote = line.split('\t')
    if iii.f_is_float(rating) and iii.f_is_int(vote):
        if float(rating) >= 6.5 and int(vote) >= 1000:
            list_ratings_out.append(movie_id + '|' + rating + '|' + vote)
            dict_ratings[movie_id] = rating + '|' + vote

#with open(directory + 'ajemdibi_ratings_out.txt', mode = 'wt', encoding = 'utf_8') as f:
#    f.writelines('\n'.join(list_ratings_out))

list_ratings_out = []
iii.f_print('Ratings process finished')
################################################################################
iii.f_print('--------')
iii.f_print('Movies process started')

for i, line in enumerate(list_movies):
    movie_id,movie_type,title,original_title,is_adult,start_year,end_year,runtime,genres = '','','','','','','','',''
    movie_id,movie_type,title,original_title,is_adult,start_year,end_year,runtime,genres = line.split('\t')
    if movie_type in ('movie', 'tvMovie', 'tvSeries', 'tvMiniSeries', 'tvSpecial') and is_adult == '0':
        if start_year  == r'\N': start_year = ''
        if genres      == r'\N': genres     = ''
        #title          =  iii.f_normalize(title)
        #original_title =  iii.f_normalize(original_title)
        list_movies_out.append(movie_id + '|' + movie_type + '|' + title + '|' + original_title + '|' + start_year + '|' + genres)
        dict_movies           [movie_id] =      movie_type + '|' + title + '|' + original_title + '|' + start_year + '|' + genres

#with open(directory + 'ajemdibi_movies_out.txt', mode = 'wt', encoding = 'utf_8') as f:
#    f.writelines('\n'.join(list_movies_out))

list_movies_out = []

iii.f_print('Movies process finished')
################################################################################

for key in dict_ratings:
    try:
        dict_out[key] = dict_ratings[key] + '|' + dict_movies[key]
    except KeyError:
        pass #dict_out[key] = dict_ratings[key] + '|'
    except:
        pass

################################################################################
iii.f_print('--------')
iii.f_print('File write started')
with open(directory + file_sql_out, mode = 'wt', encoding = 'utf_8') as f:
    f.write('truncate `tb_movie`;' + '\n')
    for key, value in dict_out.items():

        rating, vote, movie_type, title_primary, title_secondary, year, genre = value.split('|')
        title_primary_ascii   = iii.f_normalize(title_primary)
        title_secondary_ascii = iii.f_normalize(title_secondary)
        sql = ''
        sql = 'insert into `tb_movie`(`id`,`title_primary`,`title_secondary`,`title_primary_ascii`,`title_secondary_ascii`,`year`,`genre`,`rating`,`vote`,`country`) values ('+\
        "'" + key + "', " +\
        "'" + title_primary.replace("'", "''")         + "', " +\
        "'" + title_secondary.replace("'", "''")       + "', " +\
        "'" + title_primary_ascii.replace("'", "''")   + "', " +\
        "'" + title_secondary_ascii.replace("'", "''") + "', " +\
        year + ", " +\
        "'" + genre.replace(",", ", ") + "', " +\
        rating + ", " +\
        vote + ", " +\
        "'');"


        #f.write(key + '|' + value + '\n')
        f.write(sql + '\n')
    f.write('commit;' + '\n')
iii.f_print('File write finished')
################################################################################
iii.f_print('--------')
iii.f_print('Country copy started - step 1')
engine = create_engine('mysql+mysqldb://' + db_user + ':' + db_password + '@' + db_host + '/' + db_database , echo = False)
conn = engine.connect()
trans = conn.begin()
sql_dml = 'truncate `tb_country`;'
conn.execute(text(sql_dml))
sql_dml = "insert into `tb_country` (`id`, `country`) select `id`, `country` from `tb_movie` where `country` not in ('countries', '');"
conn.execute(text(sql_dml))
trans.commit()
conn.close()
iii.f_print('Country copy finished - step 1')
################################################################################
iii.f_print('--------')
iii.f_print('Database insert started')
engine = create_engine('mysql+mysqldb://' + db_user + ':' + db_password + '@' + db_host + '/' + db_database , echo = False)
conn = engine.connect()
trans = conn.begin()
sql_dml = ''
with open(directory + file_sql_out, 'r') as f:
    for sql_dml in f:
        conn.execute(text(sql_dml))
trans.commit()
conn.close()
iii.f_print('Database insert finished')
################################################################################
iii.f_print('--------')
iii.f_print('Country copy started - step 2')
engine = create_engine('mysql+mysqldb://' + db_user + ':' + db_password + '@' + db_host + '/' + db_database , echo = False)
conn = engine.connect()
trans = conn.begin()
sql_dml = "update `tb_movie`, `tb_country` set `tb_movie`.`country` = `tb_country`.`country` where `tb_movie`.`id` = `tb_country`.`id`;"
conn.execute(text(sql_dml))
trans.commit()
conn.close()
iii.f_print('Country copy finished - step 2')
################################################################################
