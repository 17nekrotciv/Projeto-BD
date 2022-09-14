-- CRIAR TABELA USERS -------------------------------------------
CREATE TABLE IF NOT EXISTS Users( Userid SERIAL NOT NULL,
login TEXT NOT NULL,
password TEXT NOT NULL,
tipo TEXT NOT NULL,
IdOriginal INT,
CONSTRAINT PK_Users PRIMARY KEY (Userid));
----------------------------------------------------------------

-- INSERIR DADOS NA TABELA USERS ---------------------------------------------------------
INSERT INTO Users (login, password, tipo, IdOriginal)
SELECT CONCAT(driverref, '_d'), MD5(driverref), 'Piloto', driverid FROM driver;

INSERT INTO Users (login, password, tipo, IdOriginal)
SELECT CONCAT(constructorref, '_c'), MD5(constructorref), 'Escuderia', constructorid FROM constructors;

INSERT INTO Users (login, password, tipo)
VALUES ('admin', MD5('admin'), 'Administrador');
-------------------------------------------------------------------------------------------

-- ADMIN CRIAR CONSTRUTORES ---------------------------------------------
INSERT INTO Constructors (constructorid, constructorref, name, nationality, url)
VALUES (217,'teste12', 'Teste12', 'Brazil', 'aausdhasdasd12');

CREATE OR REPLACE FUNCTION atualiza_usuarios_construtores() RETURNS TRIGGER
AS
$$
BEGIN
	
	INSERT INTO Users (login, password, tipo, IdOriginal)
	VALUES (CONCAT(NEW.constructorref, '_c'), MD5(NEW.constructorref), 'Escuderia', NEW.constructorid);
	
	return NULL;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_atualiza_usuarios_construtores
AFTER INSERT ON constructors
FOR EACH ROW
WHEN (pg_trigger_depth() = 0)
EXECUTE PROCEDURE atualiza_usuarios_construtores();
------------------------------------------------------------------------------------

-- ADMIN CRIAR PILOTOS ------------------------------------------------------------
INSERT INTO Driver (driverid, driverref, number, code, forename, surname, dob, nationality)
VALUES (857,'teste1', 124, 'TES1', 'Te1s', 'te1', '27/06/2022', 'Brazilian');

CREATE OR REPLACE FUNCTION atualiza_usuarios_pilotos() RETURNS TRIGGER
AS
$$
BEGIN
	
	INSERT INTO Users (login, password, tipo, IdOriginal)
	VALUES (CONCAT(NEW.driverref, '_d'), MD5(NEW.driverref), 'Piloto', NEW.driverid);
	
	return NULL;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_atualiza_usuarios_pilotos
AFTER INSERT ON driver
FOR EACH ROW
WHEN (pg_trigger_depth() = 0)
EXECUTE PROCEDURE atualiza_usuarios_pilotos();
-----------------------------------------------------------------------------

-- ESCUDERIA CONSULTAR POR FORENAME ------------------------------------------
--SELECT DISTINCT
--	CONCAT(a.forename,' ', a.surname) nome_completo,
--	a.dob data_nascimento,
--	nationality nacionalidade
--FROM driver a
--INNER JOIN results b ON (b.driverid = a.driverid)
--WHERE b.constructorid = ?
--  AND a.forename = ?; -- Substituir as ? pelos respectivos valores
------------------------------------------------------------------------------

-- OVERVIEW ADMIN -----------------------------------------------------
SELECT COUNT(driverid) total_motoristas FROM driver;
SELECT COUNT(constructorid) total_escuderias FROM constructors;
SELECT COUNT(raceid) total_corridas FROM races;
SELECT COUNT(year) total_temporadas FROM seasons;
----------------------------------------------------------------------

-- OVERVIEW ESCUDERIA TOTAL VITÓRIAS --------------------------------------
CREATE OR REPLACE FUNCTION quantidade_vitorias_escuderia(idEscuderia INTEGER) RETURNS INTEGER
AS
$$
DECLARE
	totalVitorias INTEGER;
BEGIN
	SELECT 
		COUNT(resultid) total_vitorias
	FROM results 
	WHERE position = 1
	  AND constructorid = idEscuderia INTO totalVitorias;
	
	return totalVitorias;
END
$$ LANGUAGE plpgsql;

--SELECT quantidade_vitorias_escuderia(4);
--------------------------------------------------------------------------

-- OVERVIEW ESCUDERIA QUANTIDADE DE PILOTOS DIFERENTES --------------------------------------
CREATE OR REPLACE FUNCTION quantidade_pilotos_diferentes_escuderia(idEscuderia INTEGER) RETURNS INTEGER
AS
$$
DECLARE
	totalPilotos INTEGER;
BEGIN
	SELECT 
		COUNT(DISTINCT driverid) total_pilotos
	FROM results 
	WHERE constructorid = idEscuderia INTO totalPilotos;
	
	return totalPilotos;
END
$$ LANGUAGE plpgsql;

--SELECT quantidade_pilotos_diferentes_escuderia(3);
--------------------------------------------------------------------------

-- OVERVIEW ESCUDERIA PRIMEIRO E ÚLTIMO ANO --------------------------------------
CREATE OR REPLACE FUNCTION primeiro_e_ultimo_ano_escuderia(idEscuderia INTEGER) 
RETURNS TABLE (primeiro_ano INTEGER, ultimo_ano INTEGER)
AS
$$
BEGIN
	return QUERY SELECT 
		MIN(b.year) primeiro_ano,
		MAX(b.year) ultimo_ano
	FROM results a
	INNER JOIN races b ON (b.raceid = a.raceid)
	WHERE a.constructorid = idEscuderia;
END
$$ LANGUAGE plpgsql;

--SELECT primeiro_ano, ultimo_ano FROM primeiro_e_ultimo_ano_escuderia(1);
--------------------------------------------------------------------------

-- OVERVIEW PILOTO TOTAL VITÓRIAS --------------------------------------
CREATE OR REPLACE FUNCTION quantidade_vitorias_piloto(idPiloto INTEGER) RETURNS INTEGER
AS
$$
DECLARE
	totalVitorias INTEGER;
BEGIN
	SELECT 
		COUNT(resultid) total_vitorias
	FROM results 
	WHERE position = 1
	  AND driverid = idPiloto INTO totalVitorias;
	
	return totalVitorias;
END
$$ LANGUAGE plpgsql;

--SELECT quantidade_vitorias_piloto(1);
--------------------------------------------------------------------------

-- OVERVIEW PILOTO PRIMEIRO E ÚLTIMO ANO --------------------------------------
CREATE OR REPLACE FUNCTION primeiro_e_ultimo_ano_piloto(idPiloto INTEGER) 
RETURNS TABLE (primeiro_ano INTEGER, ultimo_ano INTEGER)
AS
$$
BEGIN
	return QUERY SELECT 
		MIN(b.year) primeiro_ano,
		MAX(b.year) ultimo_ano
	FROM results a
	INNER JOIN races b ON (b.raceid = a.raceid)
	WHERE a.driverid = idPiloto;
END
$$ LANGUAGE plpgsql;

--SELECT primeiro_ano, ultimo_ano FROM primeiro_e_ultimo_ano_piloto(1);
--------------------------------------------------------------------------

-- ADMIN RELATÓRIO 1 ----------------------------------------------------
SELECT
	a.status,
	COUNT(b.resultid) total_resultados
FROM status a 
INNER JOIN results b ON (b.statusid = a.statusid)
GROUP BY (a.status, a.statusid)
ORDER BY a.statusid
-------------------------------------------------------------------------

-- ADMIN RELATÓRIO 2 ----------------------------------------------------
CREATE INDEX idx_nome_cidade ON geocities15k (name);
CREATE EXTENSION IF NOT EXISTS Cube ;
CREATE EXTENSION IF NOT EXISTS EarthDistance ; 
--SELECT 
--	b.name nome_cidade, 
--	a.name nome_aeroporto, 
--	a.iatacode codigo_iata_aeroporto,
--	a.city cidade_aeroporto,
--	a.type tipo_aeroporto,
--	earth_distance(ll_to_earth(a.latdeg, a.longdeg), ll_to_earth(b.lat, b.long)) distancia
--FROM (SELECT name, iatacode, city, latdeg, longdeg, type, isocountry FROM airports) a,
--	 (SELECT name, lat, long FROM geocities15k) b
--WHERE earth_distance(ll_to_earth(a.latdeg, a.longdeg), ll_to_earth(b.lat, b.long)) <= 100000
--  AND a.type IN ('medium_airport', 'large_airport')
--  AND a.isocountry = 'BR'
--  AND b.name = ?; -- Substituir a ? pelo respectivo valor
-------------------------------------------------------------------------

-- ESCUDERIA RELATÓRIO 3 ------------------------------------------------
CREATE INDEX idx_driverid_results ON results (driverid);
CREATE INDEX idx_constructorid_results ON results (constructorid);
CREATE OR REPLACE FUNCTION listagem_pilotos_escuderia(idEscuderia INTEGER) 
RETURNS TABLE (nome_completo TEXT, total_vitorias BIGINT)
AS
$$
BEGIN
	return QUERY SELECT
		CONCAT(a.forename, ' ', a.surname) nome_completo,
		COALESCE(COUNT(b.resultid), 0) total_vitorias
	FROM driver a 
	LEFT JOIN results b ON (b.driverid = a.driverid)
	WHERE b.position = 1
	  AND b.constructorid = idEscuderia
	GROUP BY nome_completo;
END
$$ LANGUAGE plpgsql;

--SELECT nome_completo, total_vitorias FROM listagem_pilotos_escuderia(131);
-------------------------------------------------------------------------

-- ESCUDERIA RELATÓRIO 4 ------------------------------------------------
CREATE OR REPLACE FUNCTION quantidade_resultados_status_escuderia(idEscuderia INTEGER) 
RETURNS TABLE (status TEXT, quantidade_resultados BIGINT)
AS
$$
BEGIN
	return QUERY SELECT
		a.status,
		COALESCE(COUNT(b.resultid), 0) quantidade_resultados
	FROM status a 
	LEFT JOIN results b ON (b.statusid = a.statusid)
	WHERE b.constructorid = idEscuderia
	GROUP BY a.status, a.statusid
	ORDER BY a.statusid;
END
$$ LANGUAGE plpgsql;

--SELECT status, quantidade_resultados FROM quantidade_resultados_status_escuderia(1);
-------------------------------------------------------------------------

-- PILOTO RELATÓRIO 5 ------------------------------------------------
CREATE INDEX idx_raceid_results ON results (raceid);
CREATE OR REPLACE FUNCTION quantidade_vitorias_rollup_piloto(idPiloto INTEGER) 
RETURNS TABLE (total_vitorias BIGINT, nome_corrida TEXT, ano_corrida INTEGER)
AS
$$
BEGIN
	return QUERY SELECT
		COALESCE(COUNT(a.resultid), 0) total_vitorias,
		b.name nome_corrida,
		b.year ano_corrida
	FROM results a 
	INNER JOIN races b ON (b.raceid = a.raceid)
	WHERE a.driverid = idPiloto
	  AND a.position = 1
	GROUP BY ROLLUP(nome_corrida, ano_corrida)
	ORDER BY nome_corrida;
END
$$ LANGUAGE plpgsql;

--SELECT nome_corrida, ano_corrida, total_vitorias FROM quantidade_vitorias_rollup_piloto(1);
-------------------------------------------------------------------------

-- PILOTO RELATÓRIO 6 ------------------------------------------------
CREATE OR REPLACE FUNCTION quantidade_resultados_status_piloto(idPiloto INTEGER) 
RETURNS TABLE (status TEXT, quantidade_resultados BIGINT)
AS
$$
BEGIN
	return QUERY SELECT
		a.status,
		COALESCE(COUNT(b.resultid), 0) quantidade_resultados
	FROM status a 
	LEFT JOIN results b ON (b.statusid = a.statusid)
	WHERE b.driverid = idPiloto
	GROUP BY a.status, a.statusid
	ORDER BY a.statusid;
END
$$ LANGUAGE plpgsql;

--SELECT status, quantidade_resultados FROM quantidade_resultados_status_piloto(1);
-------------------------------------------------------------------------

-- LOG TABLE ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Logs( Logid SERIAL NOT NULL,
Userid INTEGER NOT NULL,
date DATE NOT NULL,
time TIME NOT NULL,
CONSTRAINT PK_Logs PRIMARY KEY (Logid),
CONSTRAINT FK_Logs_Users FOREIGN KEY (Userid)
REFERENCES Users (Userid));

INSERT INTO Logs (Userid, date, time) VALUES (1, CURRENT_DATE, CURRENT_TIME);
-------------------------------------------------------------------------