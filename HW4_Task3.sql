--Написать SELECT-запросы, которые выведут информацию согласно инструкциям ниже.

--Внимание: результаты запросов не должны быть пустыми, при необходимости добавьте данные в таблицы.

--Количество исполнителей в каждом жанре.
select g.genre_name, count(ag.artist_id)
from genres g 
join artistgenres ag on g.genre_id = ag.genre_id 
group by g.genre_id


--Количество треков, вошедших в альбомы 2019–2020 годов.
select count(t.track_id)
from  albums a 
join tracks t on a.album_id = t.album_id 
where a.release_year between 2019 and 2020

--Средняя продолжительность треков по каждому альбому.
select a.album_name, round(avg(t.duration),0)
from  albums a 
join tracks t on a.album_id = t.album_id
group by a.album_id 


--Все исполнители, которые не выпустили альбомы в 2020 году.
select a.artist_name
from Artists a
where a.artist_id not in (
    select distinct aa.artist_id
    from ArtistAlbums aa
    join Albums al on aa.album_id = al.album_id
    where al.release_year = 2020
);

--Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
select distinct collection_name
from collections c1
join collectiontracks ct on c1.collection_id = ct.collection_id 
join tracks t on ct.track_id = t.track_id 
join albums a on t.album_id = a.album_id 
join artistalbums aa on a.album_id = aa.album_id 
join artists a2 on aa.artist_id = a2.artist_id
where a2.artist_name = 'Muse'


