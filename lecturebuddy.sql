DROP DATABASE IF lecturebuddy;
CREATE DATABASE  lecturebuddy;
\c lecturebuddy;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: choices; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE choices (
    choiceid integer NOT NULL,
    choicetext character varying(150) NOT NULL,
    questionid integer
);


ALTER TABLE public.choices OWNER TO postgres;

--
-- Name: choices_choiceid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE choices_choiceid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.choices_choiceid_seq OWNER TO postgres;

--
-- Name: choices_choiceid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE choices_choiceid_seq OWNED BY choices.choiceid;


--
-- Name: class; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE class (
    classid integer NOT NULL,
    classname character varying(100) NOT NULL,
    section integer
);


ALTER TABLE public.class OWNER TO postgres;

--
-- Name: class_classid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE class_classid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.class_classid_seq OWNER TO postgres;

--
-- Name: class_classid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE class_classid_seq OWNED BY class.classid;


--
-- Name: map_selection_ans; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE map_selection_ans (
    userid integer,
    instanceid integer,
    xco integer NOT NULL,
    yco integer NOT NULL
);


ALTER TABLE public.map_selection_ans OWNER TO postgres;

--
-- Name: map_selection_q; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE map_selection_q (
    questionid integer NOT NULL,
    question text NOT NULL,
    image character varying(100),
    adminowner integer,
    answer character varying(20)
);


ALTER TABLE public.map_selection_q OWNER TO postgres;

--
-- Name: map_selection_q_questionid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE map_selection_q_questionid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.map_selection_q_questionid_seq OWNER TO postgres;

--
-- Name: map_selection_q_questionid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE map_selection_q_questionid_seq OWNED BY map_selection_q.questionid;


--
-- Name: multiple_choice_ans; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE multiple_choice_ans (
    userid integer,
    instanceid integer,
    choiceid integer
);


ALTER TABLE public.multiple_choice_ans OWNER TO postgres;

--
-- Name: multiple_choice_q; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE multiple_choice_q (
    questionid integer NOT NULL,
    question text NOT NULL,
    image character varying(100),
    adminowner integer,
    answerid integer
);


ALTER TABLE public.multiple_choice_q OWNER TO postgres;

--
-- Name: multiple_choice_q_questionid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE multiple_choice_q_questionid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.multiple_choice_q_questionid_seq OWNER TO postgres;

--
-- Name: multiple_choice_q_questionid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE multiple_choice_q_questionid_seq OWNED BY multiple_choice_q.questionid;


--
-- Name: person; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE person (
    personid integer NOT NULL,
    firstname character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    admin boolean NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(300) NOT NULL
);


ALTER TABLE public.person OWNER TO postgres;

--
-- Name: person_class_join; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE person_class_join (
    personid integer,
    classid integer
);


ALTER TABLE public.person_class_join OWNER TO postgres;

--
-- Name: person_personid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE person_personid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.person_personid_seq OWNER TO postgres;

--
-- Name: person_personid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE person_personid_seq OWNED BY person.personid;


--
-- Name: question_instance; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE question_instance (
    instanceid integer NOT NULL,
    questionid integer NOT NULL,
    classid integer,
    questiontype character varying(100),
    date character varying(50),
    open boolean DEFAULT true
);


ALTER TABLE public.question_instance OWNER TO postgres;

--
-- Name: question_instance_instanceid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE question_instance_instanceid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.question_instance_instanceid_seq OWNER TO postgres;

--
-- Name: question_instance_instanceid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE question_instance_instanceid_seq OWNED BY question_instance.instanceid;


--
-- Name: short_answer_ans; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE short_answer_ans (
    userid integer,
    instanceid integer,
    response text NOT NULL
);


ALTER TABLE public.short_answer_ans OWNER TO postgres;

--
-- Name: short_answer_q; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE short_answer_q (
    questionid integer NOT NULL,
    question text NOT NULL,
    image character varying(100),
    adminowner integer,
    answer text
);


ALTER TABLE public.short_answer_q OWNER TO postgres;

--
-- Name: short_answer_q_questionid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE short_answer_q_questionid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.short_answer_q_questionid_seq OWNER TO postgres;

--
-- Name: short_answer_q_questionid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE short_answer_q_questionid_seq OWNED BY short_answer_q.questionid;


--
-- Name: choiceid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY choices ALTER COLUMN choiceid SET DEFAULT nextval('choices_choiceid_seq'::regclass);


--
-- Name: classid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY class ALTER COLUMN classid SET DEFAULT nextval('class_classid_seq'::regclass);


--
-- Name: questionid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY map_selection_q ALTER COLUMN questionid SET DEFAULT nextval('map_selection_q_questionid_seq'::regclass);


--
-- Name: questionid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY multiple_choice_q ALTER COLUMN questionid SET DEFAULT nextval('multiple_choice_q_questionid_seq'::regclass);


--
-- Name: personid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person ALTER COLUMN personid SET DEFAULT nextval('person_personid_seq'::regclass);


--
-- Name: instanceid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY question_instance ALTER COLUMN instanceid SET DEFAULT nextval('question_instance_instanceid_seq'::regclass);


--
-- Name: questionid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY short_answer_q ALTER COLUMN questionid SET DEFAULT nextval('short_answer_q_questionid_seq'::regclass);


--
-- Data for Name: choices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY choices (choiceid, choicetext, questionid) FROM stdin;
\.


--
-- Name: choices_choiceid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('choices_choiceid_seq', 1, false);


--
-- Data for Name: class; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY class (classid, classname, section) FROM stdin;
\.


--
-- Name: class_classid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('class_classid_seq', 1, false);


--
-- Data for Name: map_selection_ans; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY map_selection_ans (userid, instanceid, xco, yco) FROM stdin;
\.


--
-- Data for Name: map_selection_q; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY map_selection_q (questionid, question, image, adminowner, answer) FROM stdin;
\.


--
-- Name: map_selection_q_questionid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('map_selection_q_questionid_seq', 1, false);


--
-- Data for Name: multiple_choice_ans; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY multiple_choice_ans (userid, instanceid, choiceid) FROM stdin;
\.


--
-- Data for Name: multiple_choice_q; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY multiple_choice_q (questionid, question, image, adminowner, answerid) FROM stdin;
\.


--
-- Name: multiple_choice_q_questionid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('multiple_choice_q_questionid_seq', 1, false);


--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY person (personid, firstname, lastname, admin, username, password) FROM stdin;
\.


--
-- Data for Name: person_class_join; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY person_class_join (personid, classid) FROM stdin;
\.


--
-- Name: person_personid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('person_personid_seq', 1, false);


--
-- Data for Name: question_instance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY question_instance (instanceid, questionid, classid, questiontype, date, open) FROM stdin;
\.


--
-- Name: question_instance_instanceid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('question_instance_instanceid_seq', 15, true);


--
-- Data for Name: short_answer_ans; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY short_answer_ans (userid, instanceid, response) FROM stdin;
\.


--
-- Data for Name: short_answer_q; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY short_answer_q (questionid, question, image, adminowner, answer) FROM stdin;
\.


--
-- Name: short_answer_q_questionid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('short_answer_q_questionid_seq', 1, false);


--
-- Name: choices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY choices
    ADD CONSTRAINT choices_pkey PRIMARY KEY (choiceid);


--
-- Name: class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY class
    ADD CONSTRAINT class_pkey PRIMARY KEY (classid);


--
-- Name: map_selection_q_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY map_selection_q
    ADD CONSTRAINT map_selection_q_pkey PRIMARY KEY (questionid);


--
-- Name: multiple_choice_q_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY multiple_choice_q
    ADD CONSTRAINT multiple_choice_q_pkey PRIMARY KEY (questionid);


--
-- Name: person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY person
    ADD CONSTRAINT person_pkey PRIMARY KEY (personid);


--
-- Name: question_instance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY question_instance
    ADD CONSTRAINT question_instance_pkey PRIMARY KEY (instanceid);


--
-- Name: short_answer_q_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY short_answer_q
    ADD CONSTRAINT short_answer_q_pkey PRIMARY KEY (questionid);


--
-- Name: map_selection_ans_instanceid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY map_selection_ans
    ADD CONSTRAINT map_selection_ans_instanceid_fkey FOREIGN KEY (instanceid) REFERENCES question_instance(instanceid);


--
-- Name: map_selection_ans_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY map_selection_ans
    ADD CONSTRAINT map_selection_ans_userid_fkey FOREIGN KEY (userid) REFERENCES person(personid);


--
-- Name: map_selection_q_adminowner_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY map_selection_q
    ADD CONSTRAINT map_selection_q_adminowner_fkey FOREIGN KEY (adminowner) REFERENCES person(personid);


--
-- Name: multiple_choice_ans_choiceid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY multiple_choice_ans
    ADD CONSTRAINT multiple_choice_ans_choiceid_fkey FOREIGN KEY (choiceid) REFERENCES choices(choiceid);


--
-- Name: multiple_choice_ans_instanceid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY multiple_choice_ans
    ADD CONSTRAINT multiple_choice_ans_instanceid_fkey FOREIGN KEY (instanceid) REFERENCES question_instance(instanceid);


--
-- Name: multiple_choice_ans_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY multiple_choice_ans
    ADD CONSTRAINT multiple_choice_ans_userid_fkey FOREIGN KEY (userid) REFERENCES person(personid);


--
-- Name: multiple_choice_q_adminowner_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY multiple_choice_q
    ADD CONSTRAINT multiple_choice_q_adminowner_fkey FOREIGN KEY (adminowner) REFERENCES person(personid);


--
-- Name: multiple_choice_q_answerid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY multiple_choice_q
    ADD CONSTRAINT multiple_choice_q_answerid_fkey FOREIGN KEY (answerid) REFERENCES choices(choiceid);


--
-- Name: person_class_join_classid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person_class_join
    ADD CONSTRAINT person_class_join_classid_fkey FOREIGN KEY (classid) REFERENCES class(classid);


--
-- Name: person_class_join_personid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person_class_join
    ADD CONSTRAINT person_class_join_personid_fkey FOREIGN KEY (personid) REFERENCES person(personid);


--
-- Name: question_instance_classid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY question_instance
    ADD CONSTRAINT question_instance_classid_fkey FOREIGN KEY (classid) REFERENCES class(classid);


--
-- Name: short_answer_ans_instanceid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY short_answer_ans
    ADD CONSTRAINT short_answer_ans_instanceid_fkey FOREIGN KEY (instanceid) REFERENCES question_instance(instanceid);


--
-- Name: short_answer_ans_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY short_answer_ans
    ADD CONSTRAINT short_answer_ans_userid_fkey FOREIGN KEY (userid) REFERENCES person(personid);


--
-- Name: short_answer_q_adminowner_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY short_answer_q
    ADD CONSTRAINT short_answer_q_adminowner_fkey FOREIGN KEY (adminowner) REFERENCES person(personid);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

