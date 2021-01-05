CREATE TABLE user (
id int(2) not null auto_increment,
username varchar(25) not null,
email varchar (50) not null,
password varchar(80),
join_date datetime,
picture varchar(20),
primary key (id)
);
