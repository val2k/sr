CREATE TABLE stats_non_aggregated(
    time timestamptz,
    token text,
    customer varchar(50),
    content text,
    cdn integer,
    p2p integer,
    sessionDuration integer,

    PRIMARY KEY (time, customer, content)
);

CREATE TABLE stats(
    time timestamptz,
    customer varchar(50),
    content text,
    cdn integer,
    p2p integer,
    sessions integer,

    PRIMARY KEY (time, customer, content)
);