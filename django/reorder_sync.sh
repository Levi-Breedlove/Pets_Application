#!/usr/bin/env bash
set -euo pipefail

DB="db.sqlite3"
BACKUP="db.sqlite3.pre-reorder.$(date +%Y%m%d-%H%M%S).bak"

echo "⬇️  Backing up ${DB} → ${BACKUP}"
cp "$DB" "$BACKUP"

echo "🔄  Reordering pets_app_pet and syncing FKs…"
sqlite3 "$DB" <<'SQL'
PRAGMA foreign_keys = OFF;
BEGIN;

-- 1) Update vetvisit.pet_id based on old→new mapping
WITH ordered AS (
  SELECT id AS old_id,
         ROW_NUMBER() OVER (ORDER BY id) AS new_id
    FROM pets_app_pet
)
UPDATE pets_app_vetvisit
SET pet_id = (
  SELECT new_id
    FROM ordered
   WHERE ordered.old_id = pets_app_vetvisit.pet_id
)
WHERE pet_id IN (SELECT old_id FROM ordered);

-- 2) Update M2M join table
WITH ordered AS (
  SELECT id AS old_id,
         ROW_NUMBER() OVER (ORDER BY id) AS new_id
    FROM pets_app_pet
)
UPDATE pets_app_pet_breed
SET pets_app_pet_id = (
  SELECT new_id
    FROM ordered
   WHERE ordered.old_id = pets_app_pet_breed.pets_app_pet_id
)
WHERE pets_app_pet_id IN (SELECT old_id FROM ordered);

-- 3) Copy pets into a temp table (NULL id forces AUTOINCREMENT)
CREATE TABLE pets_app_pet_temp AS
SELECT NULL    AS id,
       name,
       gender,
       birth,
       owner,
       weight,
       height,
       picture,
       card_id
  FROM pets_app_pet
 ORDER BY id;

-- 4) Drop the old table
DROP TABLE pets_app_pet;

-- 5) Recreate it with an AUTOINCREMENT PK
CREATE TABLE pets_app_pet (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  name    VARCHAR(100) NOT NULL,
  gender  VARCHAR(6)   NOT NULL,
  birth   DATE,
  owner   VARCHAR(100) NOT NULL,
  weight  DECIMAL(8,2),
  height  DECIMAL(8,2),
  picture VARCHAR(255),
  card_id INTEGER,
  FOREIGN KEY(card_id) REFERENCES pets_app_vaccinationcard(id)
);

-- 6) Re‑insert data
INSERT INTO pets_app_pet (name,gender,birth,owner,weight,height,picture,card_id)
SELECT name,gender,birth,owner,weight,height,picture,card_id
  FROM pets_app_pet_temp;

-- 7) Clean up
DROP TABLE pets_app_pet_temp;

-- 8) Reset the AUTOINCREMENT counter
UPDATE sqlite_sequence
   SET seq = (SELECT MAX(id) FROM pets_app_pet)
 WHERE name = 'pets_app_pet';

COMMIT;
PRAGMA foreign_keys = ON;
SQL

echo "✅ Pets reordered and FKs synced. Backup at ${BACKUP}"
