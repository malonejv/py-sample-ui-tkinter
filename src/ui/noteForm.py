import os
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox as MessageBox
from typing import Optional
from businessLogic.noteManager import NoteManager
from entites.note import Note
from entites.user import User

from ui.appConfig import AppConfig
from ui.appStyles import AppStyles

class NoteForm:

    #Propiedades para Anchor y Sticky
    #NW     N       NE
    #W    CENTER     E
    #SW     S       SE
    manager = NoteManager()

    def __init__(self, parent, loggedUser:User, noteId:Optional[int] = None) -> None:

        self.__noteId = noteId
        self.__loggedUser = loggedUser
        self.__parent = parent
        self.__form = Toplevel()

        self.setIcon()
        
        if AppConfig().IsThemeEnabled():
            AppStyles().ConfigureStyles(self.__form)

        #Tamaño
        # self.__form.resizable(0,0)#bloqueo horizontal y vertical

        #Titulo
        title="Nueva nota"
        if noteId is not None: title = "Editar nota"
        self.__form.title(title)

        #Ubico el formulario en el centro de la pantalla
        self.__width = 650
        self.__height = 300
        screen_width = self.__form.winfo_screenwidth()
        screen_height = self.__form.winfo_screenheight()
        x = (screen_width/2) - (self.__width/2)
        y = (screen_height/2) - (self.__height/2)
        self.__form.geometry("%dx%d+%d+%d" % (self.__width, self.__height, x, y))
        self.__form.minsize(self.__width,self.__height)

        
        #Frame contenedor
        self.__frame = ttk.Frame(self.__form)
        self.__frame.pack(anchor=NW, fill=BOTH, expand=1, padx=25, pady=15)

        #Title
        self.__svTitle = StringVar()
        self.__svTitle.trace_add("write", self.txtTitle_TextChanged)
        self.__frameTitle = ttk.Frame(self.__frame)
        self.__frameTitle.pack(anchor=NW, fill=X, pady=3)
        self.__lblTitle = ttk.Label(self.__frameTitle, text="Título: ", anchor=E, width=20)
        self.__lblTitle.pack(side=LEFT)
        self.__txtTitle = ttk.Entry(self.__frameTitle, width=30, textvariable=self.__svTitle)
        self.__txtTitle.pack(side=LEFT, fill=X, expand=1, padx=25)
        
        #Description
        self.__frameDescription = ttk.Frame(self.__frame)
        self.__frameDescription.pack(anchor=NW, fill=BOTH, expand=1, pady=3)
        self.__lblDescription = ttk.Label(self.__frameDescription, text="Descripción: ", anchor=E, width=20)
        self.__lblDescription.pack(side=LEFT)
        self.__txtDescription = Text(self.__frameDescription, width=30, height=4, relief=SOLID)
        self.__txtDescription.pack(side=LEFT, fill=BOTH, expand=1, padx=25)
        
        #BUTTONS
        self.__frameButtons = ttk.Frame(self.__frame)
        self.__frameButtons.pack(side=TOP, pady=6)
        self.__btnCancel = ttk.Button(self.__frameButtons, width=15, text="Cancelar", command=self.btnCancel_Click)
        self.__btnCancel.pack(side=LEFT, padx=3)
        self.__btnSave = ttk.Button(self.__frameButtons, width=15, text="Guardar", command=self.btnSave_Click)
        self.__btnSave.pack(side=RIGHT)

        self.__LoadControls()
        
        #Caputar evento de cierre
        self.__form.protocol("WM_DELETE_WINDOW", self.__onClosing)

        #Mostrar ventana hasta que se cierre
        self.__form.mainloop()

    def txtTitle_TextChanged(self):
        pass

    def btnSave_Click(self):
        title = self.__svTitle.get()
        description = self.__txtDescription.get('1.0', END).strip('\n\r\t')

        note = Note(title=title, description=description, userId=self.__loggedUser.Id)

        if self.__noteId is None:
            count = self.manager.Create(note)
        else:
            note.Id = self.__noteId
            count = self.manager.Update(note)
          
        if count >= 1:
            response = MessageBox.showinfo("Exito", "Se guardó correctamente!")
            if(response==MessageBox.OK):
                self.__onClosing()
        else:
            MessageBox.showinfo("Error", "No se ha podido guardar la nota!")
        
    def btnCancel_Click(self):
        self.__onClosing()

    #Methods

    def setIcon(self):
        #Ruta absoluta
        rutaIcono = os.path.abspath("../notes.ico")
        if not os.path.isfile(rutaIcono):
            rutaIcono=os.path.abspath("./section22-TkinterMySql/notes.ico")

        #Icono del form
        self.__form.iconbitmap(rutaIcono)

    def __LoadControls(self):
        self.__txtTitle.delete(0)
        self.__txtDescription.delete(1.0,END)

        if self.__noteId is not None:
            note = self.manager.GetById(self.__noteId)

            if note is not None:
                self.__txtTitle.insert(0,note.Title)
                self.__txtDescription.insert(INSERT,note.Description)

    def __onClosing(self):
        self.__form.destroy()
        self.__parent.Show()
        del self