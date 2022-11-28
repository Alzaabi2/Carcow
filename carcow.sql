use CarCowDB;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS scraped;
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