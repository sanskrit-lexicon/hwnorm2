DROP TABLE if exists keydoc_glob1;
CREATE TABLE keydoc_glob1 (
 key TEXT NOT NULL,
 data TEXT NOT NULL
);
.separator "\t"
.import keydoc_glob1.txt keydoc_glob1
create index datum on keydoc_glob1(key);
pragma table_info (keydoc_glob1);
select count(*) from keydoc_glob1;
.exit
