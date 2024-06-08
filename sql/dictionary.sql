CREATE TABLE "user" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "login" VARCHAR NOT NULL,
  "hash_password" VARCHAR NOT NULL
);

CREATE TABLE "dictionary" (
    "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
    "user_id" INT NOT NULL,
    "name" VARCHAR NOT NULL,
    "glosses" JSON NOT NULL
);

CREATE TABLE "word" (
    "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
    "dict_id" INT NOT NULL,
    "text" VARCHAR NOT NULL,
    "glosses" JSON NOT NULL
);