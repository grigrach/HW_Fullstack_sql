--Написать SELECT-запросы, которые выведут информацию согласно инструкциям ниже.

--Внимание: результаты запросов не должны быть пустыми, учтите это при заполнении таблиц.

--Название и продолжительность самого длительного трека.
select track_name, duration
from tracks t 
where duration = (select max(duration) from tracks)

--Название треков, продолжительность которых не менее 3,5 минут.
select track_name, duration
from tracks t 
where duration >= 195

--Названия сборников, вышедших в период с 2018 по 2020 год включительно.
select collection_name, release_year
from collections c 
where release_year between 2018 and 2020

--Исполнители, чьё имя состоит из одного слова.
select artist_name
from artists a 
where artist_name not like '% %'

--Название треков, которые содержат слово «мой» или «my».
select track_name
from tracks t 
where track_name like '%My%' or track_name like '%мой%'