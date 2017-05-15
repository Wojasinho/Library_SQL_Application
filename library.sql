
# Create table Cathegory
CREATE TABLE CATHEGORY (
id_cathegory INT not null,
primary key (id_cathegory)
)

# Add new column "name" and add
ALTER TABLE CATHEGORY
ADD name varchar2(20)
CHECK ( name IN ('adaptation', 'autobiography', 'biography', 'classic', 'comic book','comedy', 'cookbook', 'drama', 'encyclopedia',
'fairy tale', 'fantasy novel',  'ghost story', 'historical drama', 'novel','non-fiction', 'poetry', 'romantic comedy', 'set book','short story'
,'science fiction', 'travel guide', 'textbook') );


INSERT INTO CATHEGORY (id_cathegory, name) VALUES (1, 'adaptation');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (2, 'autobiography');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (3,'biography');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (4,'classic');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (5,'comic book');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (6,'comedy');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (7,'cookbook');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (8,'drama');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (9,'encyclopedia');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (10,'fairy tale');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (11,'fantasy novel');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (12,'ghost story');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (13,'historical drama');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (14,'novel');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (15,'non-fiction');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (16,'poetry');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (17,'romantic comedy');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (18,'set book');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (19,'short story');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (20,'science fiction');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (21,'travel guide');
INSERT INTO CATHEGORY (id_cathegory, name) VALUES (22,'textbook');
