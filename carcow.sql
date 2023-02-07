use CarCowDB;

SET FOREIGN_KEY_CHECKS = 0;

-- DROP TABLE IF EXISTS scraped;
CREATE TABLE scraped (
    VIN             varchar(255) not null,
    make            varchar(255) not null,
    model           varchar(255) not null,
    year            varchar(255) not null,
    trim            varchar(255) null,
    mileage         varchar(255) not null,
    price           varchar(255) not null,
    suggested       varchar(255) not null,
    zipcode         varchar(255) null,
    url             varchar(255) not null,
    searchID        varchar(255) null,
    imageurl           varchar(255) null,
    date            DATETIME,
    PRIMARY KEY (VIN)
);

CREATE TABLE makes_ids (
    make            varchar(255) not null,
    make_id         DECIMAL not null
);

DROP TABLE IF EXISTS models_ids;
DROP TABLE IF EXISTS makes_ids;
CREATE TABLE models_ids (
    model           varchar(255) not null,
    model_id        DECIMAL not null
);
