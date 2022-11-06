-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE ProductDetails (
    pid INT NOT NULL REFERENCES Products(id),
    des VARCHAR(2000) NOT NULL,
    image VARCHAR(2083) NOT NULL
);

CREATE TABLE Sellers (
    id INT NOT NULL PRIMARY KEY GENERATED by DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id)
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    sid INT NOT NULL REFERENCES Sellers(id)
);

CREATE TABLE Inventory (
    sid INT NOT NULL REFERENCES Sellers(id),
    pid INT NOT NULL REFERENCES Products(id),
    invNum INT NOT NULL,
    PRIMARY KEY (sid,pid)
);

CREATE TABLE ProductReviews (
    pid INT NOT NULL REFERENCES Products(id),
    uid INT NOT NULL REFERENCES Users(id),
    text VARCHAR(2000) UNIQUE NOT NULL,
    numPos INT NOT NULL,
    numNeg INT NOT NULL,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    PRIMARY KEY (pid, uid)
);

CREATE TABLE SellerReviews (
    sid INT NOT NULL REFERENCES Sellers(id),
    uid INT NOT NULL REFERENCES Users(id),
    text VARCHAR(2000) UNIQUE NOT NULL,
    numPos INT NOT NULL,
    numNeg INT NOT NULL,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    PRIMARY KEY (sid, uid)
);

CREATE TABLE Line_item (
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    sid INT NOT NULL REFERENCES Sellers(id),
    num_item INT NOT NULL,
    PRIMARY KEY (uid, pid, sid)
);