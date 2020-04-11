CREATE TABLE clients (
    id SERIAL,
    login varchar NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (login)
);

CREATE TABLE wallets (
    id SERIAL,
    client_id int NOT NULL,
    currency varchar NOT NULL,
    amount decimal NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT client_id_fk FOREIGN KEY (client_id) REFERENCES clients (id)
);

CREATE TABLE history (
    id SERIAL,
    client_id int NOT NULL,
    amount decimal NOT NULL,
    datetime timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT client_id_fk FOREIGN KEY (client_id) REFERENCES clients (id)
);
