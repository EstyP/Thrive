CREATE DATABASE thrive;
USE thrive;

CREATE TABLE plants (
    plant_name varchar(100) NOT NULL,
    common_name varchar(100),
    light varchar(50) NOT NULL,
    maintenance varchar(50) NOT NULL,
    water_days int NOT NULL,
    soil_water_indicator varchar(50) NOT NULL,
    toxic varchar(10) NOT NULL,
    humidity varchar(50) NOT NULL,
    min_temp int NOT NULL,
    max_temp int NOT NULL,
    image_url varchar(100) NOT NULL,

    PRIMARY KEY (plant_name)
);

CREATE TABLE users (
    id int NOT NULL AUTO_INCREMENT,
    username varchar(50) NOT NULL,
    email varchar(100) NOT NULL,
    city varchar(100) NOT NULL,
    password varchar(150) NOT NULL,
    salt char(40) NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE user_plants (
    user_id int NOT NULL,
    plant_name varchar(100) NOT NULL,

    PRIMARY KEY (user_id, plant_name),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (plant_name) REFERENCES plants (plant_name)
);

INSERT INTO plants
(plant_name, common_name, light, maintenance, water_days, soil_water_indicator, toxic, humidity, min_temp, max_temp, image_url)
VALUES
('aglaonema', 'chinese evergreen', 'part sun', 'easy', 6, 'dry', 'yes', 'humid', 18, 25, 'aglaonema.jpg'),
('alocasia', 'elephant ear', 'full sun', 'hard', 2, 'moist', 'yes', 'high humidity', 18, 25, 'alocasia.jpg'),
('strelitzia reginae', 'orange bird of paradise', 'full sun', 'hard', 2, 'moist', 'yes', 'humid', 18, 24, 'strelitzia_reginae.png'),
('strelitzia nicolai', 'white bird of paradise', 'full sun', 'hard', 2, 'moist', 'yes', 'high humidity', 18, 24, 'strelitzia_nicolai.png'),
('philodendron', 'heart leaf', 'shade', 'easy', 6, 'dry', 'yes', 'humid', 18, 25, 'philodendron.jpg'),
('spathiphyllum wallisii', 'peace lily', 'part sun', 'medium', 2, 'moist', 'yes', 'high humidity', 18, 24, 'spathiphyllum_wallisii.jpg'),
('chlorophytum comosum', 'spider plant', 'part sun', 'easy', 6, 'dry', 'no', 'humid', 18, 25, 'chlorophytum_comosum.jpg'),
('ceropegia linearis', 'string of hearts', 'part sun', 'medium', 6, 'dry', 'no', 'humid', 18, 25, 'ceropegia_linearis.webp'),
('nephrolepis exaltata', 'sword fern', 'part sun', 'hard', 2, 'moist', 'no', 'high humidity', 15, 23, 'sword_fern.jpg'),
('zamioculcas zamiifolia', 'zz plant', 'dark', 'easy', 15, 'dry', 'yes', 'humid', 18, 25, 'zamioculcas_zamiifolia.webp'),
('pilea peperomioides', 'chinese money plant', 'part sun', 'medium', 6, 'dry', 'no', 'humid', 18, 24, 'pilea_peperomioides.webp'),
('chamaedorea elegans', 'parlor palm', 'part sun', 'medium', 6, 'dry', 'no', 'high humidity', 18, 24, 'chamaedorea_elegans.jpg'),
('monstera adansonii', 'monkey mask', 'part sun', 'hard', 6, 'dry', 'yes', 'high humidity', 18, 24, 'monstera_adansonii.jpg'),
('dracaena trifasciata', 'snake plant', 'part sun','easy', 15, 'dry', 'yes', 'dry air', 18, 25, 'dracaena_trifasciata.jpg'),
('hedera helix', 'common ivy', 'shade', 'medium', 2, 'moist', 'yes', 'high humidity', 10, 20, 'hedera_helix.jpg'),
('ficus benjamina', 'weeping fig', 'part sun', 'medium', 6, 'dry', 'yes', 'high humidity', 16, 27, 'ficus_benjamina.webp'),
('ficus microcarpa', 'ginseng ficus', 'full sun', 'hard', 6, 'dry', 'yes', 'humid', 18, 27, 'ficus_microcarpa.webp'),
('schefflera arboricola', 'umbrella tree', 'part sun', 'easy', 6, 'dry', 'yes', 'humid', 18, 25, 'umbrella_tree.jpg'),
('tradescantia', 'fantasy venice', 'part sun', 'medium', 6, 'dry', 'yes', 'humid', 18, 25, 'tradescantia.webp'),
('dionaea muscipula', 'venus fly trap', 'full sun', 'hard', 2, 'moist', 'no', 'high humidity', 18, 25, 'dionaea_muscipula.webp'),
('persea americana', 'avocado plant', 'full sun', 'hard', 6, 'dry', 'no', 'high humidity', 18, 25, 'persea_americana.jpg'),
('phalaenopsis', 'moth orchid', 'part sun', 'easy', 6, 'dry', 'no', 'high humidity', 18, 24, 'phalaenopsis.jpg'),
('dracaena draco', 'dragon tree', 'part sun', 'easy', 15, 'dry', 'yes', 'humid', 18, 25, 'dragon_tree.jpg'),
('aloe barbadensis', 'aloe vera', 'part sun', 'easy', 15, 'dry', 'yes', 'dry air', 18, 25, 'aloe_vera.jpg'),
('pothos', 'devil\'s ivy', 'part sun', 'easy', 6, 'dry', 'yes', 'humid', 18, 24, 'pothos.jpg'),
('monstera', 'swiss cheese plant', 'part sun', 'easy', 6, 'dry', 'yes', 'high humidity', 18, 25, 'monstera.jpg'),
('cactus', 'cactus', 'full sun', 'easy', 15, 'dry', 'no', 'dry air', 15, 30, 'cactus.jpg'),
('aechmea fasciata', 'bromeliads', 'part sun', 'medium', 6, 'dry', 'no', 'high humidity', 18, 30, 'bromeliads.jpeg');