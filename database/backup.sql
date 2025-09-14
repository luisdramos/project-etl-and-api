--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: etl; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA etl;


ALTER SCHEMA etl OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: charges; Type: TABLE; Schema: etl; Owner: postgres
--

CREATE TABLE etl.charges (
    id text NOT NULL,
    company_id text,
    amount numeric(16,2) NOT NULL,
    status character varying(30) NOT NULL,
    created_at date NOT NULL,
    updated_at date
);


ALTER TABLE etl.charges OWNER TO postgres;

--
-- Name: companies; Type: TABLE; Schema: etl; Owner: postgres
--

CREATE TABLE etl.companies (
    company_id text NOT NULL,
    name text
);


ALTER TABLE etl.companies OWNER TO postgres;

--
-- Name: daily_company_totals; Type: VIEW; Schema: etl; Owner: postgres
--

CREATE VIEW etl.daily_company_totals AS
 SELECT c.company_id,
    c.name,
    ch.created_at AS transaction_date,
    sum(ch.amount) AS total_amount
   FROM (etl.charges ch
     JOIN etl.companies c ON ((ch.company_id = c.company_id)))
  GROUP BY c.company_id, c.name, ch.created_at
  ORDER BY ch.created_at;


ALTER VIEW etl.daily_company_totals OWNER TO postgres;

--
-- Name: charges charges_pkey; Type: CONSTRAINT; Schema: etl; Owner: postgres
--

ALTER TABLE ONLY etl.charges
    ADD CONSTRAINT charges_pkey PRIMARY KEY (id);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: etl; Owner: postgres
--

ALTER TABLE ONLY etl.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (company_id);


--
-- Name: charges charges_company_id_fkey; Type: FK CONSTRAINT; Schema: etl; Owner: postgres
--

ALTER TABLE ONLY etl.charges
    ADD CONSTRAINT charges_company_id_fkey FOREIGN KEY (company_id) REFERENCES etl.companies(company_id);


--
-- PostgreSQL database dump complete
--

