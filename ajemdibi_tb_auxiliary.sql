use `cicamica$db_everything`;

--alter database `cicamica$db_everything` character set utf8 collate utf8_unicode_ci;

--drop table if exists `tb_auxiliary`;

create table if not exists `tb_auxiliary` (
    `id`                    varchar( 20)     not null primary key,
    `country`               varchar(200) default null,
    `movie_type`            varchar(200) default null
);


-- drop            index `idx_auxiliary_country` on `tb_auxiliary`;
-- create fulltext index `idx_auxiliary_country` on `tb_auxiliary`(`country`);