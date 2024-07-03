import flet as ft
from database import corso_DAO


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Lab O5 - segreteria studenti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        """Function that loads the graphical elements of the view"""
        # title
        self._title = ft.Text("App gestione studenti", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW with some controls

        # Row 0
        # dropdown con le materie e i codici
        self.ddCorsi = ft.Dropdown(label="corso", width=500, hint_text="Seleziona un corso")
        self.fillDdCorsi()

        # tasto per ricerca studente
        self._btnCercaIscritti = ft.ElevatedButton(text="Cerca iscritti", on_click=self._controller.handle_cercaIscritti)

        row0 = ft.Row([self.ddCorsi, self._btnCercaIscritti], alignment=ft.MainAxisAlignment.CENTER)

        # Row 1

        # campo per la matricola
        self._txt_matricola = ft.TextField(label="matricola", width=200)
        # campo per il nome
        self._txt_nome = ft.TextField(label="nome", width=200, read_only=True)
        # campo per il cognome
        self._txt_cognome = ft.TextField(label="cognome", width=200, read_only=True)
        """
        # text field for the name
        self.txt_name = ft.TextField(
            label="name",
            width=200,
            hint_text="Insert a your name"
        )
        """
        # button for the "hello" reply
        # self.btn_hello = ft.ElevatedButton(text="Hello", on_click=self._controller.handle_hello)

        row1 = ft.Row([self._txt_matricola, self._txt_nome, self._txt_cognome],
                      alignment=ft.MainAxisAlignment.CENTER)



        # Row 3
        # bottone cerca studente
        self._btnCercaStudente = ft.ElevatedButton(text="Cerca studente", on_click=self._controller.handle_cercaStudente)

        # bottone cerca corsi
        self._btnCercaCorsi = ft.ElevatedButton(text="Cerca corsi", on_click=self._controller.handle_cercaCorsi)

        # bottone iscrivi
        self._btnIscrivi = ft.ElevatedButton(text="Iscrivi", on_click=self._controller.handle_iscrivi)

        row2 = ft.Row([self._btnCercaStudente, self._btnCercaCorsi, self._btnIscrivi],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row0)
        self._page.controls.append(row1)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        """Function that opens a popup alert window, displaying a message
        :param message: the message to be displayed"""
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()

    def fillDdCorsi(self):
        corso = corso_DAO.CorsoDao()
        corsi = corso.getCorsi() # è una lista di oggetti CorsoDto
        for nome in corsi:
            # print(type(nome))
            self.ddCorsi.options.append(ft.dropdown.Option(key=nome.codins, text=nome.__str__()))

