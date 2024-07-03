import flet as ft
from database.studente_DAO import StudenteDao
from database.corso_DAO import CorsoDao

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._studenteDao = StudenteDao()
        self._corsoDao = CorsoDao()


    def handle_hello(self, e):
        """Simple function to handle a button-pressed event,
        and consequently print a message on screen"""
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()


    def handle_cercaIscritti(self, e):
        self._view._txt_nome.value = ""
        self._view._txt_cognome.value = ""
        self._view._txt_matricola.value = ""
        corso = self._view.ddCorsi.value
        #print(corso) # corso è la chiave, cioè il codice
        if corso is None or corso == "":
            self._view.create_alert("Selezionare un corso!")
            return

        #oggetto = StudenteDao()
        iscritti = self._studenteDao.getStudentiCorso(corso) # lista di oggetti studente

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ci sono {len(iscritti)} iscritti al corso:"))
        # self._view.update_page()
        for studente in iscritti:
            self._view.txt_result.controls.append(ft.Text(studente))

        self._view.update_page()


    def handle_cercaStudente(self, e):
        self._view._txt_nome.value = ""
        self._view._txt_cognome.value = ""
        self._view.txt_result.controls.clear()
        #self._view.ddCorsi.value = ""
        matricola = self._view._txt_matricola.value
        if matricola.isdigit() is False:
            self._view.create_alert("Inserire una matricola valida!")
            return False
        #oggetto = StudenteDao()
        risultato = self._studenteDao.getStudente(matricola)
        if risultato is None:
            self._view.create_alert("Studente non trovato!")
            return False

        self._view._txt_nome.value = risultato.nome
        self._view._txt_cognome.value = risultato.cognome
        self._view.update_page()


    def handle_cercaCorsi(self, e):
    # ho la matricola, prima di tutto scrivo nome e cognome studente nei textfield
    # poi altra query sql per i corsi
        self._view.txt_result.controls.clear()
        #oggetto = CorsoDao()
        flag = self.handle_cercaStudente(e)
        corsi = self._corsoDao.getCorsiStudente(self._view._txt_matricola.value)
        self._view.ddCorsi.value = ""

        if flag is False:
            return

        if len(corsi) == 0: # qui entra anche se lo studente esiste, io voglio che ci entri solo se
            # lo studente esiste ma non è iscritto a nessun corso (non so se si verifica mai)
            self._view.txt_result.controls.append(ft.Text("Non risultano corsi."))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text(f"Risultano {len(corsi)} corsi:"))
        for corso in corsi:
            self._view.txt_result.controls.append(ft.Text(f"{corso.nome} ({corso.codins})"))
        self._view.update_page()


    def handle_iscrivi(self, e):
        # devo anche fare il caso in cui uno studente è già iscritto a un corso
        flag = self.handle_cercaStudente(e)

        if flag is False:
            return

        codins = self._view.ddCorsi.value
        if codins == "" or codins is None:
            self._view.create_alert("Selezionare un corso!")
            return

        matricola = self._view._txt_matricola.value
        nome = self._view._txt_nome.value
        cognome = self._view._txt_cognome.value

        if self._studenteDao.studenteIscritto(codins, matricola):
            self._view.txt_result.controls.append(ft.Text(
                f"{nome} {cognome} ({matricola}) risulta già iscritto/a al corso {codins}."))
        else:
            self._corsoDao.iscrivi(codins, matricola)
            self._view.txt_result.controls.append(ft.Text(
                f"{nome} {cognome} ({matricola}) correttamente iscritto/a al corso {codins}."))

        self._view.update_page()


