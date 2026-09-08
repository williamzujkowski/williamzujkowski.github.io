-- Disposable synthetic lab only. Bootstrap executes as the container admin.
CREATE ROLE lab_owner NOLOGIN;
CREATE ROLE agent_reader LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE
  NOINHERIT NOREPLICATION NOBYPASSRLS;
REVOKE ALL ON DATABASE lab FROM PUBLIC;
GRANT CONNECT ON DATABASE lab TO agent_reader;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
CREATE SCHEMA inventory AUTHORIZATION lab_owner;
SET ROLE lab_owner;
BEGIN;
CREATE TABLE inventory.hosts (id integer PRIMARY KEY, name text NOT NULL);
INSERT INTO inventory.hosts VALUES (1, 'lab-router'), (2, 'lab-nas');
CREATE TABLE inventory.private_notes (note text);
CREATE SEQUENCE inventory.ticket_number;
-- No blanket grant on future tables. New data requires an explicit decision.
ALTER DEFAULT PRIVILEGES REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
CREATE FUNCTION inventory.rename_host() RETURNS text
  LANGUAGE sql SECURITY DEFINER SET search_path = pg_catalog, pg_temp
  AS 'UPDATE inventory.hosts SET name = ''changed-by-function'' WHERE id = 1 RETURNING name';
REVOKE ALL ON FUNCTION inventory.rename_host() FROM PUBLIC;
GRANT USAGE ON SCHEMA inventory TO agent_reader;
GRANT SELECT ON inventory.hosts TO agent_reader;
COMMIT;
RESET ROLE;
ALTER ROLE agent_reader SET default_transaction_read_only = on;
ALTER ROLE agent_reader SET search_path = pg_catalog, inventory;
ALTER ROLE agent_reader SET statement_timeout = '3s';
