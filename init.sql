drop table if exists users;
create table users(
  id integer primary key autoincrement,
  name text not null,
  age integer,
  sex integer,
  height real,
  weight real
);

drop table if exists actions;
create table actions(
  id integer primary key autoincrement,
  action_name text not null,
  body_part text not null
);

drop table if exists records;
create table records(
  id integer primary key autoincrement,
  body_part text not null,
  action_id integer,
  train_weight real DEFAULT 0,
  rm real DEFAULT 0,
  train_day TimeStamp NOT NULL DEFAULT (datetime('now','localtime'))
);

insert into users values(1,"张巍",33,1,178.8,78.8);

insert into actions values(1,"标准俯卧撑","胸部");
insert into actions values(2,"窄距俯卧撑","胸部");
insert into records values(1,"胸部",1,10,15,1503326966);
insert into records values(2,"胸部",2,0,10,1503326966);
