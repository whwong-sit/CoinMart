drop table if exists users;
create table users (
  username text primary key,
  password text not null,
  email text not null
);

drop table if exists user_watchlists;
create table user_watchlists(
  watchlist_id integer primary key autoincrement,
  username text not null,
  watchlist_name text not null,
  foreign key(username) references users(username)
);

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
insert into users values('admin', 'default', 'admin@uni.sydney.edu.au');
insert into users values('Test', 'Test_123', 'test@uni.sydney.edu.au');
insert into user_watchlists values(1, 'Test', 'bitcoin');
insert into user_watchlists values(2, 'Test', 'ripple');
insert into watchlist_items values('1', 'bitcoin', 'EUR', 1754.22019599, '2017-05-29 08:10:21');
insert into watchlist_items values('2', 'ripple', 'EUR', 0.3028863965, '2017-05-29 08:10:21');
insert into historical_watchlist_data values('1', 'bitcoin', 'EUR', 1754.22019599, '2017-05-29 11:51:12');
insert into historical_watchlist_data values('2', 'ripple', 'EUR', 0.3028863965, '2017-05-29 11:51:12');





