DROP TABLE IF EXISTS public.questions CASCADE;

CREATE TABLE IF NOT EXISTS public.questions
(
    "QID" integer NOT NULL,
    title text COLLATE pg_catalog."default",
    "titleSlug" text COLLATE pg_catalog."default",
    difficulty text COLLATE pg_catalog."default",
    "acceptanceRate" numeric,
    "paidOnly" boolean NOT NULL,
    "topicTags" text COLLATE pg_catalog."default",
    "categorySlug" text COLLATE pg_catalog."default",
    "Hints" text[], 
    "Companies"  text[],
    "SimilarQuestions" integer[],
    "Code" text,
    "Body" text,
    CONSTRAINT questions_pkey PRIMARY KEY ("QID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.questions
    OWNER to postgres;


ALTER TABLE questions DROP IF EXISTS search;
ALTER TABLE questions 
ADD search tsvector
GENERATED ALWAYS AS (
	setweight(to_tsvector('simple', "titleSlug"), 'A') || ' ' ||
	setweight(to_tsvector('simple', COALESCE("categorySlug", '')), 'A') || ' ' ||
	setweight(to_tsvector('simple', "topicTags"), 'A') || ' ' ||
	setweight(to_tsvector('english', "difficulty"), 'B') || ' ' ||
	setweight(to_tsvector('english', "Body"), 'B') :: tsvector
) stored;

DROP INDEX IF EXISTS public.questions_idx;

CREATE UNIQUE INDEX IF NOT EXISTS questions_idx
    ON public.questions USING btree
    ("titleSlug" COLLATE pg_catalog."default" ASC NULLS LAST, difficulty COLLATE pg_catalog."default" ASC NULLS LAST)
    INCLUDE("QID", title, "titleSlug", difficulty)
    TABLESPACE pg_default;

DROP INDEX IF EXISTS public.search_idx;

CREATE INDEX IF NOT EXISTS search_idx 
    ON questions USING GIN
    (search);

DROP TABLE IF EXISTS public.topic_tags CASCADE;

CREATE TABLE IF NOT EXISTS public.topic_tags
(
    slug text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "topicTags_pkey" PRIMARY KEY (slug)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.topic_tags
    OWNER to postgres;

DROP TABLE IF EXISTS public.categories CASCADE;

CREATE TABLE IF NOT EXISTS public.categories
(
    slug text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default",
    CONSTRAINT categories_pkey PRIMARY KEY (slug)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.categories
    OWNER to postgres;

DROP INDEX IF EXISTS public.category_slug_idx;

CREATE UNIQUE INDEX IF NOT EXISTS category_slug_idx
    ON public.categories USING btree
    (slug COLLATE pg_catalog."default" ASC NULLS LAST)
    INCLUDE(name)
    TABLESPACE pg_default;

DROP TABLE IF EXISTS public.companies;

CREATE TABLE IF NOT EXISTS public.companies
(
    slug text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default",
    "questionCount" integer,
    CONSTRAINT companies_pkey PRIMARY KEY (slug)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.companies
    OWNER to postgres;

DROP INDEX IF EXISTS public.company_slug_idx;

CREATE UNIQUE INDEX IF NOT EXISTS company_slug_idx
    ON public.companies USING btree
    (slug COLLATE pg_catalog."default" ASC NULLS LAST)
    INCLUDE(name, "questionCount")
    TABLESPACE pg_default;

DROP TABLE IF EXISTS public.question_category;

CREATE TABLE IF NOT EXISTS public.question_category
(
    id integer NOT NULL,
    "QID" integer NOT NULL,
    "categorySlug" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "questionCategory_pkey" PRIMARY KEY (id),
    CONSTRAINT "QID" FOREIGN KEY ("QID")
        REFERENCES public.questions ("QID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "categorySlug" FOREIGN KEY ("categorySlug")
        REFERENCES public.categories (slug) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.question_category
    OWNER to postgres;

DROP INDEX IF EXISTS public.question_category_idx;

CREATE INDEX IF NOT EXISTS question_category_idx
    ON public.question_category USING btree
    ("categorySlug" COLLATE pg_catalog."default" ASC NULLS LAST)
    INCLUDE("QID")
    TABLESPACE pg_default;

DROP TABLE IF EXISTS public.question_topics;

CREATE TABLE IF NOT EXISTS public.question_topics
(
    id integer NOT NULL,
    "QID" integer NOT NULL,
    "tagSlug" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT question_topics_pkey PRIMARY KEY (id),
    CONSTRAINT "QID" FOREIGN KEY ("QID")
        REFERENCES public.questions ("QID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "tagSlug" FOREIGN KEY ("tagSlug")
        REFERENCES public.topic_tags (slug) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.question_topics
    OWNER to postgres;

DROP INDEX IF EXISTS public.question_topics_idx;

CREATE INDEX IF NOT EXISTS question_topics_idx
    ON public.question_topics USING btree
    ("tagSlug" COLLATE pg_catalog."default" ASC NULLS LAST)
    INCLUDE("QID", "tagSlug")
    TABLESPACE pg_default;

CREATE OR REPLACE FUNCTION search_questions(term text)
RETURNS TABLE(
	"QID" int,
	title text,
	rank real
)
as
$$

select 
	"QID",
	title, 
	ts_rank(search, websearch_to_tsquery('english', term)) + 
	ts_rank(search, websearch_to_tsquery('simple', term)) as rank
from questions
where search @@ websearch_to_tsquery('english', term || ':*')
or search @@ websearch_to_tsquery('simple', term || ':*')
order by rank desc;

$$ language SQL;


CREATE OR REPLACE FUNCTION queried_questions_list(term text)
RETURNS json
as
$$
select array_to_json(array_agg(row_to_json(out))) from (
    with base as (select * from search_questions(term))
    select  base."QID", base.title, questions.difficulty, array_agg(topic_tags.name) as "topicTags" from base
    join questions on base."QID" = questions."QID"
    join question_topics on questions."QID" = question_topics."QID"
    join topic_tags on topic_tags.slug = question_topics."tagSlug"
    group by 1, 2, 3
) as out
$$ language SQL;


CREATE OR REPLACE FUNCTION all_questions_list(term text)
RETURNS json
as
$$
select array_to_json(array_agg(row_to_json(out))) from (
    select  questions."QID", questions.title, questions.difficulty, array_agg(topic_tags.name) as "topicTags" from questions
    join question_topics on questions."QID" = question_topics."QID"
    join topic_tags on topic_tags.slug = question_topics."tagSlug"
    group by 1, 2, 3
) as out
$$ language SQL;