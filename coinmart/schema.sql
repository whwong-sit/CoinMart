drop table if exists users;
create table users (
  username text primary key,
  password text not null,
  email text not null
);
drop table if exists user_watchlists;
create table user_watchlists(
  username text,
  watchlist_id text,
  foreign key(username) references users(username),
  primary key(username, watchlist_id)
);
drop table if exists watchlist_items;
create table watchlist_items(
  watchlist_id text,
  cryptocurrency text,
  currency text,
  value real not null,
  foreign key(watchlist_id) references user_watchlists(watchlist_id),
  primary key(watchlist_id,cryptocurrency,currency)
);

insert into users values('admin', 'default', 'admin@uni.sydney.edu.au');





