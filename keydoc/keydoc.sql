DROP TABLE if exists keydoc;
CREATE TABLE keydoc (
 key TEXT NOT NULL,
 data TEXT NOT NULL
);
.separator "\t"
.import keydoc_input.txt keydoc
create index datum on keydoc(key);
pragma table_info (keydoc);
select count(*) from keydoc;
.exit
