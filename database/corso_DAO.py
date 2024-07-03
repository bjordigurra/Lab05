# Add whatever it is needed to interface with the DB Table corso

from database.DB_connect import get_connection
from model.corso_dto import CorsoDto
class CorsoDao:

    def getCorsi(self):
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT *
        FROM corso """
        cursor.execute(query)
        result = []
        for row in cursor: # appendo alla lista il nuovo oggetto che ho creato
            # result.append(f"{row["nome"]} ({row["codins"]})")
            result.append(CorsoDto(row["codins"], row["crediti"], row["nome"], row["pd"]))
        cursor.close()
        cnx.close()
        return result

    def getCorsiStudente(self, matricola):
        """
        con una query trova tutti i corsi a cui uno studente risulta iscritto
        :param matricola:
        :return: lista di oggetti corso dello studente
        """
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT iscrizione.codins, crediti, nome, pd
        FROM iscrizione, corso
        WHERE matricola = %s and corso.codins = iscrizione.codins
        """
        cursor.execute(query, [matricola])
        result = []
        for row in cursor:
            result.append(CorsoDto(row["codins"], row["crediti"], row["nome"], row["pd"]))

        cursor.close()
        cnx.close()
        return result


    def iscrivi(self, codins, matricola):
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """ INSERT INTO iscrizione
        VALUES (%s, %s);
        """
        cursor.execute(query, [matricola, codins])
        cnx.commit() # da fare sempre, perchè modifico il database
        cursor.close()
        cnx.close()
