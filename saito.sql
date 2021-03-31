create table saito(
    mail varchar(50),
    name varchar(20) not null,
    jyusyo varchar(100) not null,
    tel varchar(20) not null,
    age varchar(11) not null,
    pw varchar(256) not null,
    salt varchar(20) not null,
    primary key(mail)
);
