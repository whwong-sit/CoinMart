drop table if exists users;
create table users (
  username text primary key,
  password text not null,
  email text not null
);

insert into users values('admin', 'default', 'admin@uni.sydney.edu.au');
insert into users values('Test', 'Test_123', 'test@gmail.com');

drop table if exists user_watchlists;
create table user_watchlists(
  watchlist_id integer primary key autoincrement,
  username text not null,
  watchlist_name text not null,
  foreign key(username) references users(username)
);

insert into user_watchlists values(1, 'admin', 'bitcoin_EUR');
insert into user_watchlists values(2, 'Test', 'bitcoin_EUR2');

drop table if exists watchlist_items;
create table watchlist_items(
  watchlist_id integer,
  cryptocurrency text,
  currency text,
  current_value real not null,
  current_time timestamp not null,
  foreign key(watchlist_id) references user_watchlists(watchlist_id),
  primary key(watchlist_id,cryptocurrency,currency)
);

insert into watchlist_items values(1, 'bitcoin', 'EUR', 0, ' ');
insert into watchlist_items values(2, 'bitcoin', 'EUR', 0, ' ');

drop table if exists historical_watchlist_data;
create table historical_watchlist_data(
  watchlist_id integer,
  cryptocurrency text,
  currency text,
  old_value real not null,
  old_time timestamp not null,
  foreign key(watchlist_id) references user_watchlists(watchlist_id),
  primary key(watchlist_id,cryptocurrency,currency)
);

insert into historical_watchlist_data values(1, 'bitcoin', 'EUR', 0, ' ');
insert into historical_watchlist_data values(2, 'bitcoin', 'EUR', 0, ' ');

