create database if not exists CAIPIAO;
use CAIPIAO;

drop table if exists sdhaoma;
create table sdhaoma
(
    period varchar(11) not null,
    date_period varchar(11) not null,
    testhaoma varchar(8) not null,
    haoma char(5) not null,
    a char(1) not null,
    b char(1) not null,
    c char(1) not null,
    ab char(2),
    ac char(2),
    bc char(2)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

