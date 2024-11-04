--Продолжаем работать со своей базой данных. В этом задании заполните базу данных из домашнего задания к занятию "Работа с SQL. Создание БД". В ней должно быть:

--не менее 4 исполнителей,
--не менее 3 жанров,
--не менее 3 альбомов,
--не менее 6 треков,
--не менее 4 сборников.

-- Загрузка данных в таблицу Genres
INSERT INTO Genres (genre_name)
VALUES
('Rock'),
('Pop'),
('Jazz');

-- Загрузка данных в таблицу Artists
INSERT INTO Artists (artist_name)
VALUES
('Muse'),
('Adele'),
('The Weeknd'),
('Miles Davis');

-- Загрузка данных в таблицу ArtistGenres
INSERT INTO ArtistGenres (artist_id, genre_id)
VALUES
(1, 1),  -- Muse исполняет Rock
(2, 2),  -- Adele исполняет Pop
(3, 2),  -- The Weeknd исполняет Pop
(4, 3);  -- Miles Davis исполняет Jazz

-- Загрузка данных в таблицу Albums
INSERT INTO Albums (album_name, release_year)
VALUES
('Simulation Theory', 2019),
('30', 2021),
('After Hours', 2020);

-- Загрузка данных в таблицу ArtistAlbums
INSERT INTO ArtistAlbums (artist_id, album_id)
VALUES
(1, 1),  -- Muse - Simulation Theory
(2, 2),  -- Adele - 30
(3, 3);  -- The Weeknd - After Hours

-- Загрузка данных в таблицу Tracks
INSERT INTO Tracks (track_name, duration, album_id)
VALUES
('The Dark Side', 215, 1),  -- 3:35 мин
('My Prophecy', 245, 1),  -- 4:05 мин
('Easy On Me', 224, 2),  -- 3:44 мин
('My Heart Will Go On', 180, 3),  -- 3:00 мин
('Blinding Lights', 200, 3),  -- 3:20 мин
('Save Your Tears', 230, 3);  -- 3:50 мин

-- Загрузка данных в таблицу Collections
INSERT INTO Collections (collection_name, release_year)
VALUES
('Greatest Hits of 2020', 2020),
('Top Pop 2021', 2021),
('Rock Classics', 2019),
('Jazz Essentials', 2021);

-- Загрузка данных в таблицу CollectionTracks
INSERT INTO CollectionTracks (track_id, collection_id)
VALUES
(1, 1),  -- The Dark Side в сборник Greatest Hits of 2020
(2, 1),  -- My Prophecy в сборник Greatest Hits of 2020
(3, 2),  -- Easy On Me в сборник Top Pop 2021
(4, 3),  -- My Heart Will Go On в сборник Rock Classics
(5, 4),  -- Blinding Lights в сборник Jazz Essentials
(6, 2);  -- Save Your Tears в сборник Top Pop 2021