create table Category(
    id serial primary key,
    name text unique not null
);

create table Value(
    id serial primary key,
    form text unique not null,
    category int references Category
);

create table AlternativeValue(
    id serial primary key,
    form text unique not null,
    same_as int references Value
);