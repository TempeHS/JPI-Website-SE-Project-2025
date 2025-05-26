-- database: /workspaces/JPI-Website-SE-Project-2025/.database/data_source.db

-- Use the ▷ button in the top right corner to run the entire file.

-- CREATE TABLE motorcycles(extID INTERGER NOT NULL PRIMARY KEY,name TEXT NOT NULL, hyperlink TEXT NOT NULL,about TEXT NOT NULL,image TEXT NOT NULL,price TEXT NOT NULL, location TEXT NOT NULL, year TEXT NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

-- DELETE FROM motorcycles;

-- (1, '1919 Powerplus', 'https://www.parkerindian.com.au/HSPP1919.html', '1919 Powerplus, older restoration. Original bike, 80Mph Corbin speedo. Fresh tyres. Aged but generally good nickel. Great Patina. A really good rally bike with everything working as it should.', 'static/images/1919Powerplus.png', 'A$55,000', 'Sydney, Australia', '1919', 'Hans Sprangers hasprang@gmail.com');
INSERT INTO motorcycles(extID, name, hyperlink, about, image, price, location, year, contact) VALUES
(2, '1927 Big Chief (74CI)', 'https://www.parkerindian.com.au/DO1927BC.html', 'Older restoration but in fantastic order. Has factory front brake, speedo, etc. Excellent running motorcycle', 'static/images/1919Powerplus.png', 'A$65,000', 'Melbourne, Victoria', '1927', 'Parker Indian Motorcycles');