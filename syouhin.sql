create table syohin(
    syohinId int(3) auto_increment,
    user_mail varchar(30) not null,
    Artist varchar(100) not null,
    cdname varchar(100) not null,
    nedan varchar(10000) not null,
    img varchar(300) not null,
    bgm varchar(300) not null,
    primary key(syohinId)
);


insert into syohin(user_mail,Artist,cdname,nedan,img,bgm) values('100','和ぬか','イージーゲーム','200','wa.png','和ぬか_イージーゲーム.mp3');
insert into syohin(user_mail,Artist,cdname,nedan,img,bgm) values('100','サイダーガール','週刊少年ゾンビ','200','sai.png','サイダー.mp3');
insert into syohin(user_mail,Artist,cdname,nedan,img,bgm) values('100','ずっと真夜中でいいのに','暗く黒く','200','zu.png','zuto.mp3');
insert into syohin(user_mail,Artist,cdname,nedan,img,bgm) values('100','凛として時雨','unravel','200','unrav.png','unravel.mp3');
insert into syohin(user_mail,Artist,cdname,nedan,img,bgm) values('100','欅坂46','アンビバレント','200','an.png','アンビバレント.mp3');
insert into syohin(user_mail,Artist,cdname,nedan,img,bgm) values('100','欅坂46','サイレントマジョリティー','200','mjyo.png','サイマジョ.mp3');
