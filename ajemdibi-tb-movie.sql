USE `patraf_moviedatabase`;

DROP TABLE IF EXISTS `tb_movie`;

CREATE TABLE IF NOT EXISTS `tb_movie` (
  `ID` int(11) NOT NULL,
  `TITLE_ORIGINAL` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `TITLE_ASCII` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `YEAR` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `GENRES` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `RATING` decimal(3,1) DEFAULT NULL,
  `VOTES` int(11) DEFAULT NULL,
  `COUNTRIES` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  FULLTEXT KEY `index_title_ascii` (`TITLE_ASCII`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



use `db_movie`;

drop table if exists `tb_movie`;

create table if not exists `tb_movie` (
  `id`             int    ( 11)     not null primary key,
  `title_original` varchar(200) default null,
  `title_ascii`    varchar(200) default null,
  `year`           varchar(  4) default null,
  `genres`         varchar(200) default null,
  `rating`         decimal(3,1) default null,
  `votes`          int    ( 11) default null,
  `countries`      varchar(200) default null,
  index `index_title_ascii` (`title_ascii`) fulltext
);




use `patraf_databasemovie`;

ALTER DATABASE `patraf_databasemovie` CHARACTER SET utf8 COLLATE utf8_unicode_ci;

drop table if exists `tb_movie_2`;

create table if not exists `tb_movie_2` (
  `id`             varchar( 20) collate utf8_unicode_ci     not null primary key,
  `title_original` varchar(200) collate utf8_unicode_ci default null,
  `title_ascii`    varchar(200) collate utf8_unicode_ci default null,
  `year`           varchar(  4) collate utf8_unicode_ci default null,
  `genres`         varchar(200) collate utf8_unicode_ci default null,
  `rating`         decimal(3,1) default null,
  `votes`          int    ( 11) default null,
  `countries`      varchar(200) collate utf8_unicode_ci default null
);

alter table  `tb_movie_2` default character set utf8 collate utf8_unicode_ci;

drop            index `index_title_ascii` on `tb_movie_2`;
create fulltext index `index_title_ascii` on `tb_movie_2`(`title_ascii`);