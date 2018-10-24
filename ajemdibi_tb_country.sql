use `cicamica$db_ajemdibi`;

alter database `cicamica$db_ajemdibi` character set utf8 collate utf8_unicode_ci;

drop table if exists `tb_country`;

create table if not exists `tb_country` (
    `id`                    varchar( 20)     not null primary key,
    `country`               varchar(200) default null
);


drop            index `idx_country` on `tb_country`;
create fulltext index `idx_country` on `tb_country`(`country`);