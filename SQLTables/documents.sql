-- Table: public.documents

-- DROP TABLE IF EXISTS public.documents;

CREATE TABLE IF NOT EXISTS public.documents
(
    doc integer NOT NULL,
    text text COLLATE pg_catalog."default" NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    num_chars integer NOT NULL,
    date date,
    id_category integer,
    CONSTRAINT documents_pkey PRIMARY KEY (doc),
    CONSTRAINT id_category FOREIGN KEY (id_category)
        REFERENCES public.categories (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.documents
    OWNER to postgres;
-- Index: fki_id_category

-- DROP INDEX IF EXISTS public.fki_id_category;

CREATE INDEX IF NOT EXISTS fki_id_category
    ON public.documents USING btree
    (id_category ASC NULLS LAST)
    TABLESPACE pg_default;