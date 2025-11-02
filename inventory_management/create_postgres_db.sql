-- SQL Script to create PostgreSQL database and user for Inventory Management System

-- Connect to PostgreSQL as a superuser (usually postgres) before running this script
-- Command to connect: psql -U postgres

-- Create the database
CREATE DATABASE inventory_management;

-- Create a dedicated user for the application
CREATE USER inventory_user WITH PASSWORD 'Jesuslove@12';

-- Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON DATABASE inventory_management TO inventory_user;

-- Connect to the newly created database
\c inventory_management

-- Grant all privileges on the public schema to the user
GRANT ALL ON SCHEMA public TO inventory_user;

-- Grant all privileges on all tables in the public schema to the user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO inventory_user;

-- Grant all privileges on all sequences in the public schema to the user
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO inventory_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO inventory_user;

-- Set default privileges for future sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO inventory_user;

-- List databases to verify creation
\l

-- List users to verify user creation
\du

-- Connect to the new database with the new user to verify access
-- \c inventory_management inventory_user