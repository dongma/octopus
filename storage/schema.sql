create table pages
(
    id      bigint(7) not null auto_increment,
    title   varchar(200),
    content text,
    created timestamp default current_timestamp,
    primary key (id)
) engine=Innodb default charset='utf8';

/* 创建douban_datahub的数据表，电影meta信息表、评论数据表 */
create table movie_meta (
    id long comment '电影id',
    movie_name varchar(100) comment '电影名称',
    year long comment '拍摄年份',
    topics varchar(200) comment '主题分类',
    writer varchar(60) comment '编剧',
    director varchar(60) comment '导演',
    actors varchar(200) comment '主要演员',
    official_site varchar(100) comment '官方网站',
    movie_making_zone varchar(60) comment '发行地',
    IMDb varchar(60) comment '电影id信息',
    movie_rate float comment '电影评分',
    votes float comment '参与评分的人数'
) engine=Innodb default charset='utf8' comment '电影元数据';

create table comment (
    data_cid long comment '影评id',
    movie_id long comment '电影id',
    user_url varchar(100) comment '豆瓣用户URL',
    nick_name varchar(100) comment '用户昵称',
    time varchar(60) comment '评论时间',
    content text comment '评论内容',
    stars long comment '星级（几颗星）',
    valid_votes int comment '投票数（有用数）'
) engine=Innodb default charset='utf8' comment '电影热评';
