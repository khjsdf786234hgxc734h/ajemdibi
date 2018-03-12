#!/bin/env python3
import imdb_process_utility as iii

file_movies  = 'imdb.title.basics.tsv.gz'
file_ratings = 'imdb.title.ratings.tsv.gz'

list_movies_out  = []
list_ratings_out = []

dict_movies      = {}
dict_ratings     = {}
dict_out         = {}

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




with open('imdb.ratings.out.txt', mode = 'wt', encoding = 'utf_8') as f:
    f.writelines('\n'.join(list_ratings_out))

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
        title          =  iii.f_normalize(title)
        original_title =  iii.f_normalize(original_title)
        list_movies_out.append(movie_id + '|' + movie_type + '|' + title + '|' + original_title + '|' + start_year + '|' + genres)
        dict_movies           [movie_id] =      movie_type + '|' + title + '|' + original_title + '|' + start_year + '|' + genres

with open('imdb.movies.out.txt', mode = 'wt', encoding = 'utf_8') as f:
    f.writelines('\n'.join(list_movies_out))

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
with open('imdb.movies.final.out.sql', mode = 'wt', encoding = 'utf_8') as f:
    for key, value in dict_out.items():

        rating, vote, movie_type, title_ascii, title_original, year, genres = value.split('|')
        sql = ''
        sql = 'insert into `tb_movie_2`(`id`,`title_original`,`title_ascii`,`year`,`genres`,`rating`,`votes`,`countries`) values ('+\
        "'" + key + "', " +\
        "'" + title_original.replace("'", "''") + "', " +\
        "'" + title_ascii.replace("'", "''") + "', " +\
        "'" + year + "', " +\
        "'" + genres + "', " +\
        rating + ", " +\
        vote + ", " +\
        "'countries');"


        #f.write(key + '|' + value + '\n')
        f.write(sql + '\n')

iii.f_print('File write finished')


