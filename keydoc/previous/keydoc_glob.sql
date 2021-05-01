DROP TABLE if exists keydoc_glob;
CREATE TABLE keydoc_glob (
 key TEXT NOT NULL,
 data TEXT NOT NULL
);
.separator "\t"
.import keydoc_glob.txt keydoc_glob
create index datum on keydoc_glob(key);
pragma table_info (keydoc_glob);
select count(*) from keydoc_glob;
.exit
