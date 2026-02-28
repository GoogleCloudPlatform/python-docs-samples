DROP TABLE IF EXISTS product_inventory;

DROP TABLE IF EXISTS product;

CREATE TABLE
    product (
        id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        category VARCHAR(255),
        color VARCHAR(255),
        embedding vector (768) GENERATED ALWAYS AS (embedding ('text-embedding-005', description)) STORED
    );

CREATE TABLE
    product_inventory (
        id INT PRIMARY KEY,
        product_id INT REFERENCES product (id),
        inventory INT,
        price DECIMAL(10, 2)
    );

INSERT INTO
    product (id, name, description, category, color)
VALUES
    (
        1,
        'Stuffed Elephant',
        'Soft plush elephant with floppy ears.',
        'Plush Toys',
        'Gray'
    ),
    (
        2,
        'Remote Control Airplane',
        'Easy-to-fly remote control airplane.',
        'Vehicles',
        'Red'
    ),
    (
        3,
        'Wooden Train Set',
        'Classic wooden train set with tracks and trains.',
        'Vehicles',
        'Multicolor'
    ),
    (
        4,
        'Kids Tool Set',
        'Toy tool set with realistic tools.',
        'Pretend Play',
        'Multicolor'
    ),
    (
        5,
        'Play Food Set',
        'Set of realistic play food items.',
        'Pretend Play',
        'Multicolor'
    ),
    (
        6,
        'Magnetic Tiles',
        'Set of colorful magnetic tiles for building.',
        'Construction Toys',
        'Multicolor'
    ),
    (
        7,
        'Kids Microscope',
        'Microscope for kids with different magnification levels.',
        'Educational Toys',
        'White'
    ),
    (
        8,
        'Telescope for Kids',
        'Telescope designed for kids to explore the night sky.',
        'Educational Toys',
        'Blue'
    ),
    (
        9,
        'Coding Robot',
        'Robot that teaches kids basic coding concepts.',
        'Educational Toys',
        'White'
    ),
    (
        10,
        'Kids Camera',
        'Durable camera for kids to take pictures and videos.',
        'Electronics',
        'Pink'
    ),
    (
        11,
        'Walkie Talkies',
        'Set of walkie talkies for kids to communicate.',
        'Electronics',
        'Blue'
    ),
    (
        12,
        'Karaoke Machine',
        'Karaoke machine with built-in microphone and speaker.',
        'Electronics',
        'Black'
    ),
    (
        13,
        'Kids Drum Set',
        'Drum set designed for kids with adjustable height.',
        'Musical Instruments',
        'Blue'
    ),
    (
        14,
        'Kids Guitar',
        'Acoustic guitar for kids with nylon strings.',
        'Musical Instruments',
        'Brown'
    ),
    (
        15,
        'Kids Keyboard',
        'Electronic keyboard with different instrument sounds.',
        'Musical Instruments',
        'Black'
    ),
    (
        16,
        'Art Easel',
        'Double-sided art easel with chalkboard and whiteboard.',
        'Arts & Crafts',
        'White'
    ),
    (
        17,
        'Finger Paints',
        'Set of non-toxic finger paints for kids.',
        'Arts & Crafts',
        'Multicolor'
    ),
    (
        18,
        'Modeling Clay',
        'Set of colorful modeling clay.',
        'Arts & Crafts',
        'Multicolor'
    ),
    (
        19,
        'Watercolor Paint Set',
        'Watercolor paint set with brushes and palette.',
        'Arts & Crafts',
        'Multicolor'
    ),
    (
        20,
        'Beading Kit',
        'Kit for making bracelets and necklaces with beads.',
        'Arts & Crafts',
        'Multicolor'
    ),
    (
        21,
        '3D Puzzle',
        '3D puzzle of a famous landmark.',
        'Puzzles',
        'Multicolor'
    ),
    (
        22,
        'Race Car Track Set',
        'Race car track set with cars and accessories.',
        'Vehicles',
        'Multicolor'
    ),
    (
        23,
        'RC Monster Truck',
        'Remote control monster truck with oversized tires.',
        'Vehicles',
        'Green'
    ),
    (
        24,
        'Train Track Expansion Set',
        'Expansion set for wooden train tracks.',
        'Vehicles',
        'Multicolor'
    );

INSERT INTO
    product_inventory (id, product_id, inventory, price)
VALUES
    (1, 1, 9, 13.09),
    (2, 2, 40, 79.82),
    (3, 3, 34, 52.49),
    (4, 4, 9, 12.03),
    (5, 5, 36, 71.29),
    (6, 6, 10, 51.49),
    (7, 7, 7, 37.35),
    (8, 8, 6, 10.87),
    (9, 9, 7, 42.47),
    (10, 10, 3, 24.35),
    (11, 11, 4, 10.20),
    (12, 12, 47, 74.57),
    (13, 13, 5, 28.54),
    (14, 14, 11, 25.58),
    (15, 15, 21, 69.84),
    (16, 16, 6, 47.73),
    (17, 17, 26, 81.00),
    (18, 18, 11, 91.60),
    (19, 19, 8, 78.53),
    (20, 20, 43, 84.33),
    (21, 21, 46, 90.01),
    (22, 22, 6, 49.82),
    (23, 23, 37, 50.20),
    (24, 24, 27, 99.27);

CREATE INDEX product_index ON product USING scann (embedding cosine)
WITH
    (num_leaves = 5);