-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : sam. 19 mars 2022 à 21:43
-- Version du serveur :  10.3.34-MariaDB-0ubuntu0.20.04.1
-- Version de PHP : 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `agence_tourisme`
--

-- --------------------------------------------------------

--
-- Structure de la table `circuit`
--

CREATE TABLE `circuit` (
  `id` int(11) NOT NULL,
  `nom` varchar(30) NOT NULL,
  `descriptif` text NOT NULL,
  `prix_circuit` float NOT NULL,
  `duree_jour` int(11) NOT NULL,
  `ville_depart` int(11) NOT NULL,
  `ville_arrivee` int(11) NOT NULL,
  `nb_place` int(11) NOT NULL,
  `date_depart` date NOT NULL,
  `date_arrivee` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `circuit`
--

INSERT INTO `circuit` (`id`, `nom`, `descriptif`, `prix_circuit`, `duree_jour`, `ville_depart`, `ville_arrivee`, `nb_place`, `date_depart`, `date_arrivee`) VALUES
(1, 'Baguette', 'Découverte française', 500, 3, 3, 1, 10, '2022-02-25', '2022-02-28'),
(2, 'EuroTour', 'Venez découvrir la splendeur de l\'Europe', 750, 10, 3, 3, 20, '2022-03-03', '2022-03-13'),
(3, 'Tour Espagnol', 'Découvrez l\'Espagne à travers ce tour unique, et vivez une experience hors du commun', 400, 4, 8, 11, 50, '2022-05-11', '2022-05-15'),
(4, 'This is America', 'Venez découvrir le pays de l\'Oncle Sam à travers un circuit parsemé d\'expérience unique et de lieux atypiques', 2500, 15, 7, 13, 30, '2022-05-11', '2022-05-26'),
(5, 'Italie comme jamais vu', 'Venez découvrir ce pays chargé d\'histoire et de culture. Nous vous proposeront de visiter les lieux incontournables et de déguster les spécialitées locales.', 500, 4, 5, 16, 6, '2022-03-02', '2022-03-06'),
(6, 'Le pays du soleil levant', 'Voyagez à travers le Japon et découvrez les richesses de sa culture et de son mode de vie.', 9000, 20, 4, 14, 40, '2022-06-09', '2022-06-29'),
(7, 'Tour de Nouvelle-Zélande ', 'Découvrez les paysages grandioses de ce pays unique à travers un tour vous proposant de visiter les lieux incontournables.', 8000, 12, 6, 15, 50, '2022-04-06', '2022-04-18');

-- --------------------------------------------------------

--
-- Structure de la table `etape`
--

CREATE TABLE `etape` (
  `id_circuit` int(11) NOT NULL,
  `id_lieu` int(11) NOT NULL,
  `date` date NOT NULL,
  `duree_en_minute` int(11) NOT NULL,
  `ordre` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `etape`
--

INSERT INTO `etape` (`id_circuit`, `id_lieu`, `date`, `duree_en_minute`, `ordre`) VALUES
(1, 9, '2022-02-25', 1440, 1),
(1, 8, '2022-02-28', 1440, 2),
(2, 9, '2022-02-25', 1440, 1),
(2, 5, '2022-02-22', 1440, 2),
(2, 13, '2022-02-22', 2880, 3),
(2, 14, '2022-02-22', 4320, 4),
(7, 19, '2022-04-05', 1440, 1),
(7, 10, '2022-04-07', 1440, 2),
(2, 11, '2022-02-28', 1440, 5),
(2, 9, '2022-02-22', 1440, 6),
(5, 13, '2022-05-18', 2880, 1),
(5, 20, '2022-05-18', 2880, 2),
(4, 17, '2022-07-27', 4320, 1),
(4, 7, '2022-07-27', 2880, 2),
(4, 21, '2022-07-27', 4320, 3),
(6, 18, '2022-08-16', 2880, 1),
(6, 6, '2022-08-18', 4320, 2),
(3, 11, '2022-05-11', 2880, 1),
(3, 15, '2022-05-15', 2880, 2);

-- --------------------------------------------------------

--
-- Structure de la table `image`
--

CREATE TABLE `image` (
  `id` int(11) NOT NULL,
  `id_lieu` int(11) NOT NULL,
  `url` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `image`
--

INSERT INTO `image` (`id`, `id_lieu`, `url`) VALUES
(1, 13, 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Colosseo_2020.jpg/280px-Colosseo_2020.jpg'),
(2, 14, 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Tour_Eiffel_Wikimedia_Commons.jpg/260px-Tour_Eiffel_Wikimedia_Commons.jpg'),
(3, 5, 'https://upload.wikimedia.org/wikipedia/commons/e/e1/Clock_Tower_-_Palace_of_Westminster%2C_London_-_September_2006.jpg'),
(4, 6, 'https://www.kanpai.fr/sites/default/files/styles/og/public/users_uploads/2064/sensoji-temple-tokyo.jpg'),
(5, 7, 'https://www.panoramadelart.com/sites/default/files/FA210-a-bartholdi-liberte.jpg'),
(6, 8, 'https://cdt31.media.tourinsoft.eu/upload/cite-espace-1.jpg'),
(7, 9, 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/St_Martial_church_in_Arnac-la-Poste_16.jpg/260px-St_Martial_church_in_Arnac-la-Poste_16.jpg'),
(8, 10, 'https://www.newzealand.com/assets/Operator-Database/img-1633906214-1424-1141-tnz-hero__aWxvdmVrZWxseQo_CropResizeWzk0MCw1MzAsNzUsImpwZyJd.jpg'),
(9, 11, 'https://upload.wikimedia.org/wikipedia/commons/5/52/Sagrada_Fam%C3%ADlia._Fa%C3%A7ana_del_Naixement_%28cropped%29.jpg'),
(10, 12, 'https://www.canadatrip.fr/images/mont-royal.jpg'),
(11, 15, 'https://d3ipks40p8ekbx.cloudfront.net/dam/jcr:b71591c8-5f8c-4fb2-a4d6-932aa2ec68e7/490x373_Madrid_Puerta%20del%20Sol-min-min.jpg'),
(12, 16, 'https://voyages.topexpos.fr/wp-content/uploads/2017/12/the-fish-market-restaurant-ottawa-930x618.jpg'),
(13, 17, 'https://cdn2.civitatis.com/estados-unidos/los-angeles/galeria/detalle-paseo-fama.jpg'),
(14, 18, 'https://upload.wikimedia.org/wikipedia/commons/e/ec/Kumamoto_Castle_05n3200.jpg'),
(15, 19, 'https://media-cdn.tripadvisor.com/media/photo-s/0e/9d/96/90/wellington-cable-car.jpg'),
(16, 20, 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Venezia_Basilica_di_San_Marco_Fassade_2.jpg/1200px-Venezia_Basilica_di_San_Marco_Fassade_2.jpg'),
(17, 21, 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Mandalay_Bay_Hotel.jpg');

-- --------------------------------------------------------

--
-- Structure de la table `lieu`
--

CREATE TABLE `lieu` (
  `id` int(11) NOT NULL,
  `id_ville` int(11) NOT NULL,
  `label` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `prix_visite` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `lieu`
--

INSERT INTO `lieu` (`id`, `id_ville`, `label`, `description`, `prix_visite`) VALUES
(5, 2, 'Big Ben', 'Big Ben est le surnom de la grande cloche de 13,5 tonnes se trouvant au sommet de la tour Élisabeth, la tour horloge du palais de Westminster, qui est le siège du Parlement britannique, à Londres. ', 40),
(6, 4, 'Sanctuaire Asakusa', 'Le Senso-ji est un temple bouddhiste situé à Tokyo, dans le quartier d\'Asakusa. C\'est le plus vieux temple de la capitale japonaise. Il est dédié à la déesse bodhisattva Kannon.', 100),
(7, 7, 'Statue de la liberté', 'La Liberté éclairant le monde, ou simplement Liberté, plus connue sous le nom de statue de la Liberté, est l\'un des monuments les plus célèbres des États-Unis. Cette statue monumentale est située à New York, sur la Liberty Island, au sud de Manhattan, à l\'embouchure de l\'Hudson et à proximité d’Ellis Island.', 50),
(8, 1, 'Cité de l espace', 'La Cité de l\'espace est un centre de culture scientifique orienté vers l\'espace et la conquête spatiale, consacré autant à l\'astronomie qu\'à l\'astronautique. Située à Toulouse, la Cité de l\'espace a été inaugurée en juin 1997.', 60),
(9, 3, 'Église Saint Martial', 'Le bâtiment est un exemple d\'église fortifiée. Elle possède des contreforts surmontés d\'échauguettes cylindriques. Elle était entourée d\'une muraille dont subsiste une tour carrée, munie de créneaux et de mâchicoulis. L\'intérieur de l\'église possède un reliquaire émaillé datant du XIIIe siècle', 0),
(10, 6, 'SkyTower', 'La Sky Tower est une tour située dans le centre-ville d\'Auckland, et qui sert d\'émetteur pour la radio et la télévision.', 25),
(11, 8, 'Sagrada Familia', 'La Sagrada Família, Temple Expiatori de la Sagrada Família de son nom complet en catalan, ou Templo Expiatorio de la Sagrada Familia en espagnol est une basilique de Barcelone dont la construction a commencé en 1882. C’est l’un des exemples les plus connus du modernisme catalan et un monument emblématique de la ville.', 60),
(12, 9, 'Mont Royale', 'Le Mont Royal est une colline qui domine la ville de Montréal, au Québec. Il s\'agit de l\'une des dix collines montérégiennes situées dans le sud-ouest de la province.', 20),
(13, 5, 'Colisée', 'Le Colisée, à l\'origine amphithéâtre Flavien, est un immense amphithéâtre ovoïde situé dans le centre de la ville de Rome, entre l\'Esquilin et le Cælius, le plus grand jamais construit dans l\'Empire romain. Il est l\'une des plus grandes œuvres de l\'architecture et de l\'ingénierie romaines.', 75),
(14, 10, 'Tour Eiffel', 'La Tour Eiffel est une tour de fer puddlé de 324 mètres de hauteur située à Paris, à l’extrémité nord-ouest du parc du Champ-de-Mars en bordure de la Seine dans le 7ème arrondissement. Son adresse officielle est 5, avenue Anatole-France.', 30),
(15, 11, 'Puerta del Sol', 'La Puerta del Sol est située au cœur de Madrid, dans l\'arrondissement du Centre, à 800 m à l\'est du Palais royal et au nord-est de la Plaza Mayor.', 0),
(16, 12, 'Marche By', 'Le Marché By est un quartier animé qui accueille des marchés fermiers en plein air et des épiceries spécialisées vendant du fromage canadien et du chocolat infusé à l\'érable. Il est également connu pour son art de rue coloré et ses magasins branchés proposant de l\'artisanat et des vêtements de créateurs locaux. ', 0),
(17, 13, 'Hollywood Boulevard', 'Hollywood Boulevard est l’une des plus célèbres avenues du quartier de Hollywood, dans la ville américaine de Los Angeles en Californie. Haut lieu du tourisme de la ville, le boulevard s\'étend d\'Est en Ouest de Vermont Avenue jusqu\'à Sunset Boulevard.', 0),
(18, 14, 'Château de Kumamoto', 'Le château de Kumamoto est un château en hauteur situé à Kumamoto dans la préfecture du même nom au Japon. C\'était un grand château extrêmement bien fortifié. Le tenshu a été partiellement rénové en 1960 mais les plus anciennes poutres de bois ont été laissées sur place.', 40),
(19, 15, 'Wellington Cable Car', 'Le téléphérique de Wellington est un funiculaire à Wellington, en Nouvelle-Zélande, entre Lambton Quay, la principale rue commerçante, et Kelburn, une banlieue dans les collines surplombant le centre-ville, culminant à 120 m sur une longueur de 612 m. ', 50),
(20, 16, 'Basilique Saint Marc', 'La basilique cathédrale Saint-Marc, à Venise, est la plus importante basilique de Venise. Construite en 828, reconstruite après l\'incendie qui ravagea le palais des Doges en 976, elle est, depuis 1807, la cathédrale du patriarche de Venise.', 30),
(21, 17, 'Mandalay Bay Resort and Casino', 'Le Mandalay Bay Resort and Casino est un hôtel de luxe de 39 étages avec casino, situé sur le Las Vegas Strip à Paradise. Il est détenu et exploité par MGM Resorts International. Les cinq derniers étages de la tour sont occupés par un hôtel Four Seasons.', 100);

-- --------------------------------------------------------

--
-- Structure de la table `pays`
--

CREATE TABLE `pays` (
  `id` int(11) NOT NULL,
  `nom` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `pays`
--

INSERT INTO `pays` (`id`, `nom`) VALUES
(1, 'France'),
(2, 'Angleterre'),
(3, 'Japon'),
(4, 'Espagne'),
(5, 'Italie'),
(6, 'Etats-Unis'),
(7, 'Nouvelle-Zélande'),
(8, 'Canada');

-- --------------------------------------------------------

--
-- Structure de la table `reservation`
--

CREATE TABLE `reservation` (
  `id_circuit` int(11) NOT NULL,
  `id_utilisateur` int(11) NOT NULL,
  `nb_place` int(11) NOT NULL,
  `date` date NOT NULL,
  `heure` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `reservation`
--

INSERT INTO `reservation` (`id_circuit`, `id_utilisateur`, `nb_place`, `date`, `heure`) VALUES
(1, 2, 1, '2022-01-10', '10:18:21'),
(3, 4, 1, '2022-03-02', '11:33:58'),
(7, 4, 5, '2022-03-01', '19:57:14'),
(7, 4, 5, '2022-03-12', '20:20:02'),
(1, 10, 5, '2022-03-14', '19:09:19'),
(2, 12, 4, '2022-03-14', '21:25:57'),
(1, 15, 2, '2022-03-16', '15:52:43'),
(6, 15, 5, '2022-03-16', '15:53:02'),
(4, 6, 2, '2022-03-18', '10:34:13'),
(1, 6, 2, '2022-03-18', '10:37:34'),
(5, 6, 3, '2022-03-18', '10:42:33');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `id` int(11) NOT NULL,
  `role_admin` tinyint(1) NOT NULL,
  `nom` varchar(30) NOT NULL,
  `prenom` varchar(30) NOT NULL,
  `date_naissance` date DEFAULT NULL,
  `login` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mdp` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`id`, `role_admin`, `nom`, `prenom`, `date_naissance`, `login`, `email`, `mdp`) VALUES
(1, 1, 'Dupond', 'Bertrand', '1975-01-11', 'Bertrand35000', 'bertrand@gmail.com', 'BertrandDeRennes'),
(2, 0, 'Ardisson', 'Pierrick', '1960-12-07', 'Ardisonic', 'Ardisson@outlook.fr', 'ArdissonDuplateau'),
(4, 0, 'Gastembourgeois', 'CharlesDeViconte', '1991-08-08', 'Charlos', 'Charle@outlook.fr', 'Leroicestmoi'),
(6, 0, 'test', 'te', NULL, 'test2', 'test@test.com', '$2b$12$2gwrCIizx9.E2Lpm1GTO7.u6r4BeTNnON3phIHqeUqJMReyCNWqNu'),
(7, 0, 'Toto', 'Toto', NULL, 'Toto', 'Toto@toto.com', '$2b$12$ynad8v/8wP2ml7s..c.eZu8MDyPVKbYrn2KnAg7XOIjUKAq9LTK3W'),
(10, 0, 'test', 'test', NULL, 'test5', 'test5@test.com', '$2b$12$f3e.R2CJeNRT8p0AU2EkkO.o9zo4dwSmhoVJfh3iHtNDldQo9g3tW'),
(11, 0, 'toto', 'toto', NULL, 'toto2', 'Toto2@toto.com', '$2b$12$d4aWkRVbXSxDCNsP5wBwmuhro4m75JT/KWak7MSvBoIClcuyUQQOW'),
(12, 0, 'azerty', 'azerty', NULL, 'azerty', 'azerty@gmail.com', '$2b$12$gdqD4qmSaTel62i3pspUMOoTwbwtaR9RtPHfrigvxGFbSYo6WWu1W'),
(14, 0, 't', 't', '2022-03-16', 't', 'test@test.com', '$2b$12$XQONfSwwb1eVvCrp4l9qY.vA9TkioEnM1WG5LGgWudgLz5FgbXpVO'),
(15, 0, 'j', 'j', '2022-03-16', 'j', 'j@j.com', '$2b$12$JNZ6eITfNpO4VAfqdRnyDeaKPBrv5whb4E2EbKX7EL4mfNx/ZuFUe');

-- --------------------------------------------------------

--
-- Structure de la table `ville`
--

CREATE TABLE `ville` (
  `id` int(11) NOT NULL,
  `nom` varchar(30) NOT NULL,
  `id_pays` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `ville`
--

INSERT INTO `ville` (`id`, `nom`, `id_pays`) VALUES
(1, 'Toulouse', 1),
(2, 'Londres', 2),
(3, 'Arnac-la-Poste', 1),
(4, 'Tokyo', 3),
(5, 'Rome', 5),
(6, 'Auckland', 7),
(7, 'New-York', 6),
(8, 'Barcelone', 4),
(9, 'Montreal', 8),
(10, 'Paris', 1),
(11, 'Madrid', 4),
(12, 'Ottawa', 8),
(13, 'Los Angeles', 6),
(14, 'Kumamoto', 3),
(15, 'Wellington', 7),
(16, 'Venise', 5),
(17, 'Las Vegas', 6);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `circuit`
--
ALTER TABLE `circuit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_ville_arrivee` (`ville_arrivee`),
  ADD KEY `FK_ville_depart` (`ville_depart`);

--
-- Index pour la table `etape`
--
ALTER TABLE `etape`
  ADD KEY `FK_id_circuit` (`id_circuit`),
  ADD KEY `FK_id_lieu` (`id_lieu`);

--
-- Index pour la table `image`
--
ALTER TABLE `image`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_lieu` (`id_lieu`);

--
-- Index pour la table `lieu`
--
ALTER TABLE `lieu`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_ville` (`id_ville`);

--
-- Index pour la table `pays`
--
ALTER TABLE `pays`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `reservation`
--
ALTER TABLE `reservation`
  ADD KEY `FK_circuit` (`id_circuit`),
  ADD KEY `FK_utilisateur` (`id_utilisateur`);

--
-- Index pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `ville`
--
ALTER TABLE `ville`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK-pays` (`id_pays`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `circuit`
--
ALTER TABLE `circuit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT pour la table `image`
--
ALTER TABLE `image`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT pour la table `lieu`
--
ALTER TABLE `lieu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT pour la table `pays`
--
ALTER TABLE `pays`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT pour la table `ville`
--
ALTER TABLE `ville`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `circuit`
--
ALTER TABLE `circuit`
  ADD CONSTRAINT `FK_ville_arrivee` FOREIGN KEY (`ville_arrivee`) REFERENCES `ville` (`id`),
  ADD CONSTRAINT `FK_ville_depart` FOREIGN KEY (`ville_depart`) REFERENCES `ville` (`id`);

--
-- Contraintes pour la table `etape`
--
ALTER TABLE `etape`
  ADD CONSTRAINT `FK_id_circuit` FOREIGN KEY (`id_circuit`) REFERENCES `circuit` (`id`),
  ADD CONSTRAINT `FK_id_lieu` FOREIGN KEY (`id_lieu`) REFERENCES `lieu` (`id`);

--
-- Contraintes pour la table `image`
--
ALTER TABLE `image`
  ADD CONSTRAINT `FK_lieu` FOREIGN KEY (`id_lieu`) REFERENCES `lieu` (`id`);

--
-- Contraintes pour la table `lieu`
--
ALTER TABLE `lieu`
  ADD CONSTRAINT `FK_ville` FOREIGN KEY (`id_ville`) REFERENCES `ville` (`id`);

--
-- Contraintes pour la table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `FK_circuit` FOREIGN KEY (`id_circuit`) REFERENCES `circuit` (`id`),
  ADD CONSTRAINT `FK_utilisateur` FOREIGN KEY (`id_utilisateur`) REFERENCES `utilisateur` (`id`);

--
-- Contraintes pour la table `ville`
--
ALTER TABLE `ville`
  ADD CONSTRAINT `FK-pays` FOREIGN KEY (`id_pays`) REFERENCES `pays` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
