CREATE DATABASE BartendAI;

\c BartendAI;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INT,
    idDrink INT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE cocktails (
    id SERIAL PRIMARY KEY,
    drink_name VARCHAR(255),
    date_modified TIMESTAMP,
    id_drink INT,
    alcoholic VARCHAR(50),
    category VARCHAR(50),
    drink_thumb VARCHAR(255),
    glass VARCHAR(50),
    iba VARCHAR(50),
    ingredient1 VARCHAR(255),
    ingredient2 VARCHAR(255),
    ingredient3 VARCHAR(255),
    ingredient4 VARCHAR(255),
    ingredient5 VARCHAR(255),
    ingredient6 VARCHAR(255),
    ingredient7 VARCHAR(255),
    ingredient8 VARCHAR(255),
    ingredient9 VARCHAR(255),
    ingredient10 VARCHAR(255),
    ingredient11 VARCHAR(255),
    ingredient12 VARCHAR(255),
    ingredient13 VARCHAR(255),
    ingredient14 VARCHAR(255),
    ingredient15 VARCHAR(255),
    -- Ajoutez des colonnes pour chaque ingrédient jusqu'à ingredient15
    measure1 VARCHAR(255),
    measure2 VARCHAR(255),
    measure3 VARCHAR(255),
    measure4 VARCHAR(255),
    measure5 VARCHAR(255),
    measure6 VARCHAR(255),
    measure7 VARCHAR(255),
    measure8 VARCHAR(255),
    measure9 VARCHAR(255),
    measure10 VARCHAR(255),
    measure11 VARCHAR(255),
    measure12 VARCHAR(255),
    measure13 VARCHAR(255),
    measure14 VARCHAR(255),
    measure15 VARCHAR(255),
    -- Ajoutez des colonnes pour chaque mesure jusqu'à measure15
    instructions TEXT,
    video_url VARCHAR(255)
);