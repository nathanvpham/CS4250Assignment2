-- Table: public.index

-- DROP TABLE IF EXISTS public.index;

CREATE TABLE IF NOT EXISTS public.index
(
    term text COLLATE pg_catalog."default" NOT NULL,
    id_doc integer NOT NULL,
    count integer NOT NULL,
    CONSTRAINT index_pkey PRIMARY KEY (term, id_doc),
    CONSTRAINT id_doc FOREIGN KEY (id_doc)
        REFERENCES public.documents (doc) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT term FOREIGN KEY (term)
        REFERENCES public.terms (term) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.index
    OWNER to postgres;
-- Index: fki_id_doc

-- DROP INDEX IF EXISTS public.fki_id_doc;

CREATE INDEX IF NOT EXISTS fki_id_doc
    ON public.index USING btree
    (id_doc ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: fki_term

-- DROP INDEX IF EXISTS public.fki_term;

CREATE INDEX IF NOT EXISTS fki_term
    ON public.index USING btree
    (term COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;