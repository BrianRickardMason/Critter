DROP DATABASE IF EXISTS critter;

CREATE DATABASE critter
    WITH OWNER = postgres
        ENCODING = 'UTF8'
        TABLESPACE = pg_default
        LC_COLLATE = 'en_US.UTF-8'
        LC_CTYPE = 'en_US.UTF-8'
        CONNECTION LIMIT = -1
    TEMPLATE template0
;

DROP USER IF EXISTS crittuser;

CREATE USER brian WITH PASSWORD 'crittpassword';

