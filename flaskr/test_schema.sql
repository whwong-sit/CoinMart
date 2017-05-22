drop table if exists users;
create table users (
  username text primary key,
  password text not null,
  email text not null
);

insert into users values('admin', 'default', 'admin@uni.sydney.edu.au');

insert into users values('test', 'test123', 'test@uni.sydney.edu.au');

