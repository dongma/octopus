create table pages
(
    id      bigint(7) not null auto_increment,
    title   varchar(200),
    content text,
    created timestamp default current_timestamp,
    primary key (id)
) engine=Innodb default charset='utf8';
