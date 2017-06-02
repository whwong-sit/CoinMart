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
  time_stamp text not null,
  foreign key(watchlist_id) references user_watchlists(watchlist_id),
  primary key(watchlist_id,cryptocurrency,currency)
);
drop table if exists historical_watchlist_data;
create table historical_watchlist_data(
  watchlist_id text,
  cryptocurrency text,
  currency text,
  old_value real not null,
  old_time_stamp text not null,
  foreign key(watchlist_id) references user_watchlists(watchlist_id),
  primary key(watchlist_id,cryptocurrency,currency)
);


insert into historical_watchlist_data values('bitcoin', 'Bitcoin', 'EUR', 1754.22019599, '01 Jun 2017 03:15:40 PM');
insert into historical_watchlist_data values('ripple', 'Ripple', 'EUR', 0.3028863965, '01 Jun 2017 03:15:40 PM');
insert into users values('admin', 'default', 'admin@uni.sydney.edu.au');
insert into users values('Test', 'Test_123', 'test@uni.sydney.edu.au');
insert into user_watchlists values('Test', 'bitcoin');
insert into user_watchlists values('Test', 'ripple');
insert into watchlist_items values('bitcoin', 'Bitcoin', 'EUR', 1754.22019599, '01 Jun 2017 03:15:40 PM');
insert into watchlist_items values('ripple', 'Ripple', 'EUR', 0.3028863965, '01 Jun 2017 03:15:40 PM');
select * from user_watchlists, watchlist_items where user_watchlists.watchlist_id = watchlist_items.watchlist_id and user_watchlists.username = 'Test'