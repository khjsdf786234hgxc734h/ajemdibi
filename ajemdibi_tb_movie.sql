use `cicamica$db_everything`;

alter database `cicamica$db_everything` character set utf8 collate utf8_unicode_ci;

drop table if exists `tb_movie`;

create table if not exists `tb_movie` (
    `id`                    varchar( 20)     not null primary key,
    `title_primary`         varchar(200) default null,
    `title_secondary`       varchar(200) default null,
    `title_primary_ascii`   varchar(200) default null,
    `title_secondary_ascii` varchar(200) default null,
    `year`                  int    (  4) default null,
    `genre`                 varchar(200) default null,
    `rating`                decimal(3,1) default null,
    `vote`                  int    ( 11) default null,
    `country`               varchar(200) default null
);


--drop            index `idx_title_primary_ascii`      on `tb_movie`;
create fulltext index `idx_title_primary_ascii`      on `tb_movie`(`title_primary_ascii`);
--drop            index `idx_title_secondary_ascii`    on `tb_movie`;
create fulltext index `idx_title_secondary_ascii`    on `tb_movie`(`title_secondary_ascii`);
create fulltext index `idx_country`                  on `tb_movie`(`country`);

SELECT T.table_name, CCSA.character_set_name
FROM   information_schema.`TABLES` T,
       information_schema.`COLLATION_CHARACTER_SET_APPLICABILITY` CCSA
WHERE CCSA.collation_name = T.table_collation
  AND T.table_schema = 'cicamica$db_ajemdibi'
--  AND T.table_name = 'tb_movie'
;


SELECT table_name, column_name, character_set_name, collation_name
FROM information_schema.`COLUMNS`
WHERE table_schema = 'cicamica$db_ajemdibi'
--  AND table_name = "tablename"
--  AND column_name = "columnname"
;




