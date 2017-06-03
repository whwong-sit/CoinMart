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
  watchlist_id text,
  foreign key(username) references users(username),
   PRIMARY KEY (username,watchlist_id)
);

drop table if exists userwatchlists;
create table userwatchlists(
  username text,
  watchlist_id text,
  currency2 text,
  foreign key(username) references users(username),
  PRIMARY KEY (username,watchlist_id,currency2)
);

drop table if exists watchlist_items;
create table watchlist_items(
  watchlist_id text,
  cryptocurrency text,
  currency text,
  value real not null,
  foreign key(watchlist_id) references user_watchlists(watchlist_id),
  PRIMARY KEY (watchlist_id,cryptocurrency,currency)
);
insert into watchlist_items values('bitcoin', 'Bitcoin', 'EUR', 1754.22019599);
insert into watchlist_items values('ripple', 'Ripple', 'EUR', 0.3028863965);




