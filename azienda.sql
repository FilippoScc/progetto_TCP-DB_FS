-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Nov 20, 2023 alle 18:22
-- Versione del server: 10.4.28-MariaDB
-- Versione PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `azienda`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `dipendenti_filippo_sacchetti`
--

CREATE TABLE `dipendenti_filippo_sacchetti` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `indirizzo` varchar(1024) NOT NULL,
  `telefono` varchar(100) NOT NULL,
  `agente` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dump dei dati per la tabella `dipendenti_filippo_sacchetti`
--

INSERT INTO `dipendenti_filippo_sacchetti` (`id`, `nome`, `indirizzo`, `telefono`, `agente`) VALUES
(1, 'Mario Rossi', 'Via Roma, 123', '+39 123 456789', 1),
(2, 'Lorenzo Galli', 'Via Rolo, 456', '+39 987 654321', 2),
(3, 'Luigi Verdi', 'Via Napoli, 789', '+39 555 123456', 1),
(4, 'Giovanna Russo', 'Via Firenze, 321', '+39 789 987654', 3),
(5, 'Roberto Esposito', 'Via Palermo, 654', '+39 333 777888', 2),
(6, 'Elena Ferrari', 'Via Torino, 987', '+39 222 555444', 1),
(7, 'Antonio Marino', 'Via Venezia, 222', '+39 111 999000', 3),
(8, 'Sara Giallo', 'Via Bologna, 333', '+39 444 666333', 2),
(9, 'Paolo Marrone', 'Via Genova, 555', '+39 666 111222', 1),
(10, 'Teresa Azzurro', 'Via Cagliari, 777', '+39 888 222111', 3);

-- --------------------------------------------------------

--
-- Struttura della tabella `zone_di_lavoro`
--

CREATE TABLE `zone_di_lavoro` (
  `id_zona` int(11) NOT NULL,
  `nome_zona` varchar(20) NOT NULL,
  `numero_clienti` int(11) NOT NULL,
  `id_dipendente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `zone_di_lavoro`
--

INSERT INTO `zone_di_lavoro` (`id_zona`, `nome_zona`, `numero_clienti`, `id_dipendente`) VALUES
(1, 'Ufficio Contabilità', 50, 1),
(2, 'Reparto Vendite', 30, 2),
(3, 'Magazzino', 10, 3),
(4, 'Reparto IT', 20, 4),
(5, 'Risorse Umane', 20, 5),
(6, 'Reparto Logistica', 25, 6),
(7, 'Sala Conferenze', 15, 7),
(8, 'Reparto Marketing', 12, 8),
(9, 'Reparto Ricerca & Sv', 10, 9),
(10, 'Caffetteria', 10, 10);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `dipendenti_filippo_sacchetti`
--
ALTER TABLE `dipendenti_filippo_sacchetti`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `zone_di_lavoro`
--
ALTER TABLE `zone_di_lavoro`
  ADD PRIMARY KEY (`id_zona`),
  ADD KEY `id_dipendente` (`id_dipendente`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `dipendenti_filippo_sacchetti`
--
ALTER TABLE `dipendenti_filippo_sacchetti`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT per la tabella `zone_di_lavoro`
--
ALTER TABLE `zone_di_lavoro`
  MODIFY `id_zona` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `zone_di_lavoro`
--
ALTER TABLE `zone_di_lavoro`
  ADD CONSTRAINT `zone_di_lavoro_ibfk_1` FOREIGN KEY (`id_dipendente`) REFERENCES `dipendenti_filippo_sacchetti` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
