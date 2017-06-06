
drop table if exists users;
create table users (
  username text primary key,
  password text not null,
  email text not null
);

insert into users values('admin', 'default', 'admin@uni.sydney.edu.au');

drop table if exists user_watchlists;
create table user_watchlists(
  username text,
  watchlist_name text,
  foreign key(username) references users(username),
  PRIMARY KEY (username,watchlist_name)
);

drop table if exists watchlist_items;
create table watchlist_items(
  username text,
  watchlist_name text,
  cryptocurrency text,
  currency text,
  current_value real not null,
  current_time timestamp not null,
  foreign key(watchlist_name,username) references user_watchlists(watchlist_name,username),
  primary key(username,watchlist_name,cryptocurrency,currency)
);

drop table if exists historical_watchlist_data;
create table historical_watchlist_data(
  username text,
  watchlist_name text,
  cryptocurrency text,
  currency text,
  old_value real not null,
  old_time timestamp not null,
  foreign key(watchlist_name,username) references user_watchlists(watchlist_name,username),
  primary key(username,watchlist_name,cryptocurrency,currency)
);





