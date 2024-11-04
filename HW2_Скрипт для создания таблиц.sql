-- Таблица для жанров
CREATE TABLE Genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL
);

-- Таблица для исполнителей
CREATE TABLE Artists (
    artist_id SERIAL PRIMARY KEY,
    artist_name VARCHAR(100) NOT NULL
);

-- Таблица для связи исполнителей и жанров (многие ко многим)
CREATE TABLE ArtistGenres (
    artist_id INT REFERENCES Artists(artist_id) ON DELETE CASCADE,
    genre_id INT REFERENCES Genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (artist_id, genre_id)
);

-- Таблица для альбомов
CREATE TABLE Albums (
    album_id SERIAL PRIMARY KEY,
    album_name VARCHAR(100) NOT NULL,
    release_year INT NOT NULL
);

-- Таблица для связи исполнителей и альбомов (многие ко многим)
CREATE TABLE ArtistAlbums (
    artist_id INT REFERENCES Artists(artist_id) ON DELETE CASCADE,
    album_id INT REFERENCES Albums(album_id) ON DELETE CASCADE,
    PRIMARY KEY (artist_id, album_id)
);

-- Таблица для треков
CREATE TABLE Tracks (
    track_id SERIAL PRIMARY KEY,
    track_name VARCHAR(100) NOT NULL,
    duration INT NOT NULL,
    album_id INT REFERENCES Albums(album_id) ON DELETE CASCADE
);

-- Таблица для сборников
CREATE TABLE Collections (
    collection_id SERIAL PRIMARY KEY,
    collection_name VARCHAR(100) NOT NULL,
    release_year INT NOT NULL
);

-- Таблица для связи треков и сборников (многие ко многим)
CREATE TABLE CollectionTracks (
    track_id INT REFERENCES Tracks(track_id) ON DELETE CASCADE,
    collection_id INT REFERENCES Collections(collection_id) ON DELETE CASCADE,
    PRIMARY KEY (track_id, collection_id)
);