drop table if exists watchlists;
create table watchlists (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);
drop table if exists users;
create table users (
  username text primary key,
  password text not null,
  email text not null
);

