
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


insert into cathegory
values (1,'adaptation');
