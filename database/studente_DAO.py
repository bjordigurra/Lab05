# Add whatever it is needed to interface with the DB Table studente

from database.DB_connect import get_connection
from model.studente_dto import StudenteDto

class StudenteDao:

    def getStudente(self, matricola):
        """
        fa una query al database cercando lo studente che corrisponde a una data matricola
        :param matricola: matricola dello studente da cercare
        :return: l'oggetto studente se la matricola esiste, None altrimenti
        """
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT *
        FROM studente
        WHERE matricola = %s
        """
        cursor.execute(query, [matricola])
        result = None

        for row in cursor: # se il risultato è un database vuoto, non entra mai nel ciclo!!! (verificato io)
            result = StudenteDto(row["matricola"], row["nome"], row["cognome"], row["CDS"])

        cursor.close()
        cnx.close()
        return result  # lo studente se lo ha trovato, o None se non l'ha trovato



    def getStudentiCorso(self, ins): # ins è l'oggetto insegnamento
        """
        Con query sql trova tutti gli studenti iscritti a un corso
        :param ins: stringa con il codice del corso
        :return: lista di oggetti studente iscritti al corso
        """
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)
        # query che prende studenti e relative iscrizioni per ciascuno, posso
        query = """ SELECT iscrizione.matricola, nome, cognome, CDS, iscrizione.codins
                FROM studente, iscrizione
                WHERE studente.matricola = iscrizione.matricola and iscrizione.codins = %s
        """
        cursor.execute(query, [ins])
        result = []
        for row in cursor:
            #print(row)
            result.append(StudenteDto(row["matricola"], row["nome"], row["cognome"], row["CDS"]))

        cursor.close()
        cnx.close()
        return result

    def studenteIscritto(self, codins, matricola):
        # ritorna True se studente già iscritto a un corso, False altrimenti
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT *
        FROM iscrizione
        WHERE codins = %s AND matricola = %s
        """
        cursor.execute(query, [codins, matricola])

        for row in cursor:
            return True # se entra nel ciclo ci sarà solo un record, quindi ritorna direttamente True
        # perchè lo studente maricola è già iscritto al corso codins

        return False # se non entra nel ciclo vuol dire che non è iscritto e quindi ritorna False



