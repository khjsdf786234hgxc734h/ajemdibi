#!/bin/env python3
import ajemdibi_process_utility as iii
import shutil
import urllib.request

file_movies  = 'ajemdibi_movies_tsv.gz'
file_ratings = 'ajemdibi_ratings_tsv.gz'

url_movies   = 'https://datasets.imdbws.com/title.basics.tsv.gz'
url_ratings  = 'https://datasets.imdbws.com/title.ratings.tsv.gz'

list_movies_out  = []
list_ratings_out = []

dict_movies      = {}
dict_ratings     = {}
dict_out         = {}



iii.f_print('--------')

iii.f_print('Movies file download started')
#f = open(file_name, 'bw')
with urllib.request.urlopen(url_movies) as response, open(file_movies, 'wb') as f:
    shutil.copyfileobj(response, f)
#f.close()
iii.f_print('Movies file download finished')

iii.f_print('---------')

iii.f_print('Ratings file download started')
with urllib.request.urlopen(url_ratings) as response, open(file_ratings, 'wb') as f:
    shutil.copyfileobj(response, f)
iii.f_print('Ratings file download finished')

iii.f_print('---------')

iii.f_print('Ratings file read started')
list_ratings = iii.f_read_gzip_file(file_ratings)
iii.f_print('Ratings file read finished')


iii.f_print('--------')

iii.f_print('Movies file read started')
list_movies = iii.f_read_gzip_file(file_movies)
iii.f_print('Movies file read finished')


iii.f_print('--------')


iii.f_print('Ratings process started')

for i, line in enumerate(list_ratings):
    movie_id, rating, vote = '','',''
    movie_id, rating, vote = line.split('\t')
    if iii.f_is_float(rating) and iii.f_is_int(vote):
        if float(rating) >= 6.5 and int(vote) >= 1000:
            list_ratings_out.append(movie_id + '|' + rating + '|' + vote)
            dict_ratings[movie_id] = rating + '|' + vote

#with open('ajemdibi_ratings_out.txt', mode = 'wt', encoding = 'utf_8') as f:
#    f.writelines('\n'.join(list_ratings_out))

list_ratings_out = []
iii.f_print('Ratings process finished')


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

#with open('ajemdibi_movies_out.txt', mode = 'wt', encoding = 'utf_8') as f:
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


iii.f_print('File write started')
with open('ajemdibi_movies_final_out.sql', mode = 'wt', encoding = 'utf_8') as f:
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
        "'" + genre + "', " +\
        rating + ", " +\
        vote + ", " +\
        "'countries');"


        #f.write(key + '|' + value + '\n')
        f.write(sql + '\n')

iii.f_print('File write finished')
