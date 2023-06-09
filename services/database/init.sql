--
-- PostgreSQL database dump
--

-- Dumped from database version 14.7
-- Dumped by pg_dump version 14.7

-- Started on 2023-05-27 15:10:14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3325 (class 1262 OID 16395)
-- Name: postomats; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE postomats WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'ru_RU.UTF-8';

ALTER DATABASE postomats OWNER TO root;

\connect postomats

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 210 (class 1259 OID 16558)
-- Name: rawdataset; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rawdataset (
    usertext text NOT NULL,
    mark text NOT NULL,
    adress text NOT NULL,
    reviewdate timestamp without time zone NOT NULL,
    clusternumber integer NOT NULL,
    article text NOT NULL,
    seller text NOT NULL,
    longitude double precision NOT NULL,
    latitude double precision NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.rawdataset OWNER TO root;

--
-- TOC entry 212 (class 1259 OID 16588)
-- Name: rawdataset_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rawdataset_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rawdataset_id_seq OWNER TO root;

--
-- TOC entry 3326 (class 0 OID 0)
-- Dependencies: 212
-- Name: rawdataset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rawdataset_id_seq OWNED BY public.rawdataset.id;


--
-- TOC entry 209 (class 1259 OID 16407)
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    usertext text NOT NULL,
    mark text NOT NULL,
    adress text NOT NULL,
    reviewdate timestamp without time zone NOT NULL,
    clusternumber integer NOT NULL,
    article text NOT NULL,
    seller text NOT NULL,
    longitude double precision NOT NULL,
    latitude double precision NOT NULL,
    classnumber integer NOT NULL
);


ALTER TABLE public.reviews OWNER TO root;

--
-- TOC entry 211 (class 1259 OID 16567)
-- Name: xdataset; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.xdataset (
    usertext text NOT NULL,
    mark text NOT NULL,
    adress text NOT NULL,
    reviewdate timestamp without time zone NOT NULL,
    clusternumber integer NOT NULL,
    article text NOT NULL,
    seller text NOT NULL,
    longitude double precision NOT NULL,
    latitude double precision NOT NULL,
    classnumber integer NOT NULL
);


ALTER TABLE public.xdataset OWNER TO root;

--
-- TOC entry 3172 (class 2604 OID 16589)
-- Name: rawdataset id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rawdataset ALTER COLUMN id SET DEFAULT nextval('public.rawdataset_id_seq'::regclass);


--
-- TOC entry 3317 (class 0 OID 16558)
-- Dependencies: 210
-- Data for Name: rawdataset; Type: TABLE DATA; Schema: public; Owner: postgres
--

--
-- TOC entry 3327 (class 0 OID 0)
-- Dependencies: 212
-- Name: rawdataset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rawdataset_id_seq', 29749, true);


--
-- TOC entry 3174 (class 2606 OID 16413)
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (seller, article, usertext, adress, reviewdate, longitude, latitude);


--
-- TOC entry 3176 (class 2606 OID 16596)
-- Name: xdataset xdataset_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xdataset
    ADD CONSTRAINT xdataset_pkey PRIMARY KEY (usertext, mark, reviewdate, adress, article, clusternumber, seller, longitude, latitude, classnumber);


-- Completed on 2023-05-27 15:10:15

--
-- PostgreSQL database dump complete
--

