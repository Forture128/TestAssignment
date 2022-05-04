create table country
(
    id                  uuid    not null
        constraint country_pkey
            primary key,
    inserted_at         timestamp,
    updated_at          timestamp,
    inserted_by         varchar(500),
    updated_by          varchar(500),
    is_deleted          boolean not null,
    name                varchar(120),
    confirmed           integer,
    recovered           integer,
    deaths              integer,
    population          bigint,
    sq_km_area          double precision,
    life_expectancy     varchar(10),
    elevation_in_meters varchar(120),
    continent           varchar(120),
    abbreviation        varchar(120),
    location            varchar(120),
    iso                 integer,
    capital_city        varchar(120),
    lat                 varchar(120),
    long                varchar(120),
    updated             timestamp
);

alter table country
    owner to zymo;

create unique index ix_country_id
    on country (id);

create table region
(
    id          uuid    not null
        constraint region_pkey
            primary key,
    inserted_at timestamp,
    updated_at  timestamp,
    inserted_by varchar(500),
    updated_by  varchar(500),
    is_deleted  boolean not null,
    country_id  uuid
        constraint region_country_id_fkey
            references country,
    name        varchar(120),
    lat         varchar(120),
    long        varchar(120),
    confirmed   integer,
    recovered   integer,
    deaths      integer,
    updated     timestamp
);

alter table region
    owner to zymo;

create unique index ix_region_id
    on region (id);

