alter table structure drop constraint structure_ibfk_1;
alter table structure drop constraint structure_ibfk_2;
alter table tags drop constraint tags_ibfk_1;
alter table price drop constraint price_ibfk_1;
drop table if exists address;
drop table if exists layout;
drop table if exists house;
drop table if exists tags;
drop table if exists structure;
drop table if exists price;
drop table if exists user;
create table layout(
id int not null auto_increment,
lname varchar(10),
primary key(id)
);



create table house(
id int primary key not null auto_increment,
name varchar(30),
square varchar(20),
city varchar(10),
town varchar(10),
detail varchar(50),
sellingstatus varchar(10),
housetype varchar(10)
);
create table structure(
hid int not null,
lid int not null,
primary key(hid,lid),
foreign key(lid) references layout(id),
foreign key(hid) references house(id)
);

create table tags(
hid int not null,
tag varchar (20),
primary key (hid,tag),
foreign key (hid) references house(id)
);
create table price(
hid int not null,
pricetype varchar(16),
value int,
foreign key (hid) references house(id)
);
create table user(
id int not null auto_increment,
username varchar(20) unique not null, 
password varchar(20) not null,
primary key (id)
);
insert into layout values(1,"1室");
insert into layout values(2,"2室");
insert into layout values(3,"3室");
insert into layout values(4,"4室");
insert into layout values(5,"5室");
insert into layout values(6,"6室");
insert into layout values(7,"7室");
insert into layout values(8,"8室");
insert into layout values(9,"9室");
insert into layout values(10,"10室");
insert into layout values(11,"商业");
insert into layout values(12,"别墅");