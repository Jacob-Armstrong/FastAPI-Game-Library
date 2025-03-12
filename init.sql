-- Create table on startup
CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    rating DECIMAL(2, 1) NOT NULL,
    publisher TEXT NOT NULL
);

-- Secondary index on game title
CREATE INDEX index_title
ON games(title);

-- Insert dummy data
INSERT INTO games (title, description, rating, publisher) VALUES
('Minecraft', 'Explore your own unique worlds, survive the night, and create anything you can imagine!', 5, 'Xbox Game Studios'),
('Starfield', 'Starfield is the first new universe in 25 years from Bethesda Game Studios, the award-winning creators of The Elder Scrolls V: Skyrim and Fallout 4.', 2.9, 'Bethesda Game Studios'),
('Skyrim', 'The next chapter in the highly anticipated Elder Scrolls saga arrives from the makers of the 2006 and 2008 Games of the Year, Bethesda Game Studios.', 4.7, 'Bethesda Game Studios'),
('Baldur''s Gate 3', 'Baldur’s Gate 3 is a story-rich, party-based RPG set in the universe of Dungeons & Dragons, where your choices shape a tale of fellowship and betrayal, survival and sacrifice, and the lure of absolute power.', 4.8, 'Larian Studios');

-- Create table on startup
CREATE TABLE IF NOT EXISTS publishers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    games TEXT NOT NULL
);

-- Secondary index on publisher name
CREATE INDEX index_name
ON publishers(name);

-- Insert dummy data
INSERT INTO publishers (name, description, games) VALUES
('Xbox Game Studios', 'Xbox Game Studios is an American video game publisher based in Redmond, Washington. It was established in March 2000, spun out from an internal Games Group, for the development and publishing of video games for Microsoft Windows.', 'Minecraft, Forza Horizon 5, Halo Infinite'),
('Bethesda Game Studios', 'Bethesda Game Studios is an American video game developer and a studio of ZeniMax Media based in Rockville, Maryland. It is best known for its action role-playing franchises, including The Elder Scrolls, Fallout, and Starfield.', 'The Elder Scrolls, Fallout, Starfield'),
('Larian Studios', 'Larian Studios is a Belgian independent video game developer and publisher founded in 1996 by Swen Vincke. It is best known for developing the Divinity series and Baldur''s Gate 3.', 'Baldur''s Gate 3');


