CREATE TABLE IF NOT EXISTS vote_session (
   id serial PRIMARY KEY,
   vote_id VARCHAR (255) NOT NULL UNIQUE,
   psw VARCHAR (255) NOT NULL,
   create_date VARCHAR (255)
);

CREATE TABLE IF NOT EXISTS otp (
   id serial PRIMARY KEY,
   vote_id VARCHAR (255) NOT NULL,
   otp VARCHAR (255) NOT NULL,
   status VARCHAR (255) NOT NULL,
   create_date VARCHAR (255)
);

CREATE TABLE IF NOT EXISTS secret (
   id serial PRIMARY KEY,
   vote_id VARCHAR (255) NOT NULL,
   secret VARCHAR (255) NOT NULL,
   status VARCHAR (255) NOT NULL,
   create_date VARCHAR (255)
);

show tables;
