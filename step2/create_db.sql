USE guidebook;

CREATE TABLE IF NOT EXISTS plants (
    id_plant INT AUTO_INCREMENT PRIMARY KEY,
    plant_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    properties TEXT,
    harvest_season VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS medicines (
    id_medicine INT AUTO_INCREMENT PRIMARY KEY,
    medicine_name VARCHAR(255) NOT NULL,
    active_component TEXT,
    plant_ids INT,
    description TEXT,
    application_methods TEXT,
    dosage DECIMAL(10,2),
    manufacturing_date DATE,
    expiration_date DATE,
    cost DECIMAL(10,2),
    FOREIGN KEY (plant_ids) REFERENCES plants(id_plant)
);

INSERT INTO plants (plant_name, scientific_name, properties, harvest_season) 
VALUES
    ('Будра плющевидная', 'Glechoma hederacea', 'Противовоспалительные свойства', 'Весна-лето'),
    ('Шалфей лекарственный', 'Salvia officinalis', 'Антисептические свойства', 'Лето-осень'),
    ('Мать-и-мачеха', 'Tussilago farfara', 'Отхаркивающие свойства', 'Весна'),
    ('Череда', 'Bídens', 'Общеукрепляющие свойства', 'Лето-осень'),
    ('Мелисса', 'Melissa officinalis', 'Спазмолитические свойства', 'Лето');

INSERT INTO medicines (medicine_name, active_component, plant_ids, description, application_methods, dosage, manufacturing_date, expiration_date, cost)
VALUES
    ('Фитогель', 'Флавоноиды', '1', 'Противовоспалительное средство', 'Пероральное применение', 2.5, '2023-01-01', '2024-01-01', 10.50),
    ('Шалфейник', 'Танины', '2', 'Противовоспалительное и антисептическое средство', 'Чай', 1.5, '2023-02-01', '2024-02-01', 15.75),
    ('Мать-и-мачехин сироп', 'Слизи', '3', 'Отхаркивающее средство', 'Пероральное применение', 3.0, '2023-03-01', '2024-03-01', 12.25),
    ('Чередовит', 'Витамины', '4', 'Общеукрепляющее средство', 'Пероральное применение', 1.8, '2023-04-01', '2024-04-01', 8.90),
    ('Мелиссин бальзам', 'Эфирное масло мелиссы', '5', 'Спазмолитическое средство', 'Наружное применение', 2.0, '2023-05-01', '2024-05-01', 14.00);


INSERT INTO medicines (medicine_name, active_component, plant_ids, description, application_methods, dosage, manufacturing_date, expiration_date, cost)
VALUES
    ('Мелиссин чай', 'Эфирное масло мелиссы', '5', 'Спокойствие и расслабление', 'Чай', 1.5, '2023-06-01', '2024-06-01', 9.99),
    ('Шалфейное масло', 'Эфирное масло шалфея', '2', 'Для ванн и массажа', 'Наружное применение', 1.0, '2023-07-01', '2024-07-01', 18.50),
    ('Мать-и-мачехин бальзам', 'Слизи', '3', 'Для местного применения', 'Наружное применение', 2.2, '2023-08-01', '2024-08-01', 14.75),
    ('Сироп отхаркивающий', 'Флавоноиды', '1', 'Противовоспалительное и антисептическое средство', 'Пероральное применение', 3.5, '2023-09-01', '2024-09-01', 11.20),
    ('Мелиссин эликсир', 'Эфирное масло мелиссы', '5', 'Укрепление нервной системы', 'Пероральное применение', 2.8, '2023-10-01', '2024-10-01', 22.30);




