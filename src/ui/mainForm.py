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
from ui.noteForm import NoteForm

class MainForm:

    #Propiedades para Anchor y Sticky
    #NW     N       NE
    #W    CENTER     E
    #SW     S       SE

    __noteManager = NoteManager()

    __notesId = {}
    

    def __init__(self, parent, loggedUser:User) -> None:

        self.__loggedUser = loggedUser
        self.__parent = parent
        self.__form = Toplevel()

        self.setIcon()
        
        if AppConfig().IsThemeEnabled():
            AppStyles().ConfigureStyles(self.__form)

        #Tamaño
        # self.__form.resizable(0,0)#bloqueo horizontal y vertical

        #Titulo
        self.__form.title("Quick Notes")

        #Ubico el formulario en el centro de la pantalla
        self.__width = 650
        self.__height = 550
        screen_width = self.__form.winfo_screenwidth()
        screen_height = self.__form.winfo_screenheight()
        x = (screen_width/2) - (self.__width/2)
        y = (screen_height/2) - (self.__height/2)
        self.__form.geometry("%dx%d+%d+%d" % (self.__width, self.__height, x, y))
        self.__form.minsize(self.__width,self.__height)

        #Context Menu
        self.__contextMenu = Menu(self.__form, tearoff=False)
        self.__contextMenu.add_command(label="Editar nota", command=self.contextMenu_EditNote)
        self.__contextMenu.add_command(label="Eliminar Nota", command=self.contextMenu_DeleteNote)
        self.__form.config(menu=self.__contextMenu)

        #Menu
        self.__menu = Menu(self.__form)
        self.__form.config(menu=self.__menu)
        
        self.__sessionMenu = Menu(self.__menu, tearoff=False)
        self.__menu.add_cascade(label="Sesión", menu=self.__sessionMenu)
        self.__sessionMenu.add_command(label="Cerrar sesión", command=self.sesionMenu_CloseSession)
        self.__sessionMenu.add_command(label="Salir", command=self.sesionMenu_Exit)
        
        self.__notesMenu = Menu(self.__menu, tearoff=False)
        self.__menu.add_cascade(label="Notas", menu=self.__notesMenu)
        self.__notesMenu.add_command(label="Nueva nota", command=self.notesMenu_NewNote)
        
        #Container Frame
        # self.__frameContainer = ttk.Frame(self.__form)
        # self.__frameContainer.pack(anchor=NW, fill=BOTH, expand=1, pady=0)

        self.__frameControls = ttk.Frame(self.__form)
        self.__frameControls.pack(side=TOP, anchor=NW, fill=BOTH, expand=1, padx=25, pady=25)
        
        #Dummy frame
        self.__frameDummyTop = ttk.Frame(self.__frameControls, height=2)
        self.__frameDummyTop.pack(side=TOP, anchor=NW, fill=BOTH, expand=1, pady=20)

        #Title
        self.__svQuickNote = StringVar()
        self.__svQuickNote.trace_add("write", self.txtQuickNote_TextChanged)
        self.__frameQuickNote = ttk.Frame(self.__frameControls, height=1)
        self.__frameQuickNote.pack(side=TOP, anchor=NW, fill=X, expand=1, pady=3)
        self.__lblQuickNote = ttk.Label(self.__frameQuickNote, text="Nota rápida: ", width=20)
        self.__lblQuickNote.pack(side=LEFT, anchor=NE)
        self.__txtQuickNote = ttk.Entry(self.__frameQuickNote, width=30, textvariable=self.__svQuickNote)
        self.__txtQuickNote.pack(side=LEFT, anchor=NW, fill=X, expand=1)

        #Lista de notas
        self.__frameListNotes = ttk.Frame(self.__frameControls)
        self.__frameListNotes.pack(fill=BOTH, expand=1)
        self.__lblNotes = ttk.Label(self.__frameListNotes, text="Notas: ", width=20)
        self.__lblNotes.pack(side=LEFT, anchor=NE)
        self.__lstNotes = Listbox(self.__frameListNotes, width=60, height=20)
        self.__lstNotes.pack(side=LEFT, anchor=NW, fill=BOTH, expand=1)
        self.__lstNotes.bind("<Button-3>", self.__ShowContextMenu)
        self.__scrollbar = Scrollbar(self.__frameListNotes)
        self.__scrollbar.pack(side = RIGHT, fill = Y)
        self.__lstNotes.config(yscrollcommand = self.__scrollbar.set)
        self.__scrollbar.config(command = self.__lstNotes.yview)

        #Botones 
        self.__frameButtons = ttk.Frame(self.__frameControls, height=1)
        self.__frameButtons.pack(anchor=NW, fill=X, expand=1, pady=5)
        self.__btnEdit = ttk.Button(self.__frameButtons, text="Modificar", command=self.btnEdit_Click
                              , width=15)
        self.__btnEdit.pack(side=RIGHT, anchor=E)
        self.__btnDelete = ttk.Button(self.__frameButtons, text="Eliminar", command=self.btnDelete_Click
                                , width=15)
        self.__btnDelete.pack(side=RIGHT, anchor=E, padx=6)
        self.__btnNew = ttk.Button(self.__frameButtons, text="Nueva nota", command=self.btnNew_Click
                             , width=15)
        self.__btnNew.pack(side=RIGHT, anchor=E, padx=6)
        
        #Dummy frame
        self.__frameDummyBottom = ttk.Frame(self.__frameControls, height=2)
        self.__frameDummyBottom.pack(anchor=NW, fill=BOTH, expand=1, pady=20)

        #Status bar
        self.__frameStatusBar = ttk.Frame(self.__form, height=1)
        self.__frameStatusBar.pack(side=BOTTOM, anchor=S, fill=X, expand=1)
        self.__statusSesionLabel = ttk.Label(self.__frameStatusBar, text=f"Usuario: {self.__loggedUser.Email}", border=1, relief=SUNKEN)
        self.__statusSesionLabel.pack(side=BOTTOM, anchor=S, fill=X, expand=1, ipadx=4, ipady=3)


        self.__LoadControls()
                
        #Bindings
        self.__form.protocol("WM_DELETE_WINDOW", self.__onClosing)
        # self.__form.bind.bind("<FocusIn>", self.__onShowing)
        # self.__form.bind("<Visibility>", self.__onShowing)
        self.__form.bind("<Control-n>", self.__OpenNoteForm)
        self.__form.bind("<Control-r>", self.__LoadNotes)
        
        #Mostrar ventana hasta que se cierre
        self.__form.mainloop()


    #Events
    
    def sesionMenu_Preferences(self):
        pass

    def sesionMenu_CloseSession(self):
        self.__onClosing()

    def sesionMenu_Exit(self):
        self.__form.destroy()
        self.__parent.Quit()
        del self

    def notesMenu_NewNote(self):
        self.__OpenNoteForm()

    def btnNew_Click(self):
        self.__OpenNoteForm()

    def btnEdit_Click(self):
        self.__EditNote()

    def btnDelete_Click(self):
        self.__DeleteNote()

    def contextMenu_EditNote(self):
        self.__EditNote()

    def contextMenu_DeleteNote(self):
        self.__DeleteNote()

    def txtQuickNote_TextChanged(self, *args):
        title = self.__svQuickNote.get()
        if len(title.strip())>0:
            self.__form.bind("<Return>", self.__QuickNote)
        else:
            self.__form.unbind("<Return>")

    #Methods
    

    def setIcon(self):
        #Ruta absoluta
        rutaIcono = os.path.abspath("../notes.ico")
        if not os.path.isfile(rutaIcono):
            rutaIcono=os.path.abspath("./section22-TkinterMySql/notes.ico")

        #Icono del form
        self.__form.iconbitmap(rutaIcono)

    def __LoadControls(self):
        if self.__loggedUser is not None:
            self.__LoadNotes()

    def __ShowContextMenu(self, e):
        if self.__lstNotes.size() > 0:
            nearestIndex=self.__lstNotes.nearest(e.y)
            self.__lstNotes.selection_clear(0,END)
            self.__lstNotes.selection_set(nearestIndex)
            self.__lstNotes.activate(nearestIndex)
            selectedNote = self.__lstNotes.get(ACTIVE)
            if selectedNote is not None:
                self.__contextMenu.tk_popup(e.x_root, e.y_root)

    def __EditNote(self):
        selectedNote = self.__lstNotes.index(ACTIVE)
        noteId=self.__notesId[selectedNote]
        self.__OpenNoteForm(noteId)

    def __DeleteNote(self):
        resultado = MessageBox.askyesno("Confirmar", "¿Está seguro que desea eliminar la nota?")
        if(resultado):    
            selectedNote = self.__lstNotes.index(ACTIVE)
            noteId = noteId=self.__notesId[selectedNote]
            note=self.__noteManager.GetById(noteId)
            count = self.__noteManager.Delete(note)
            
            if count >= 1:
                self.__LoadNotes()
    
    def __LoadNotes(self):
        self.__notesId.clear()
        self.__lstNotes.delete(0,'end')
        notes = self.__noteManager.GetByUser(self.__loggedUser.Id)

        if len(notes)>0:
            i = 0
            for note in notes:
                self.__notesId[i]=note.Id
                self.__lstNotes.insert(i,f"{i+1} - { note.Title}")
                i+=1
            self.__lstNotes.select_set(0)
            self.__lstNotes.activate(0)
        self.__EnsureEditAndDeleteState()

    def __EnsureEditAndDeleteState(self):
        size = self.__lstNotes.size()
        selectedItem = self.__lstNotes.get(ACTIVE)
        if size>0 and selectedItem != "":
            self.__btnEdit["state"] = NORMAL        
            self.__btnDelete["state"] = NORMAL        
            self.__form.bind("<Control-e>", self.__EditNote)
            self.__form.bind("<Control-d>", self.__DeleteNote)
        else:
            self.__btnEdit["state"] = DISABLED
            self.__btnDelete["state"] = DISABLED
            self.__form.unbind("<Control-e>")
            self.__form.unbind("<Control-d>")

    def __OpenNoteForm(self, noteId:Optional[int]=None):
        self.__form.withdraw()
        NoteForm(self, self.__loggedUser, noteId)

    def __QuickNote(self, e):
        title = self.__svQuickNote.get()
        
        note = Note(title=title, userId=self.__loggedUser.Id)
        count = self.__noteManager.Create(note)
        
        if count >= 1:
            self.__svQuickNote.set("")
            self.__LoadNotes()

    def __onShowing(self,e):
        MessageBox.showinfo("On Showing")
        self.__LoadControls()
        
    def __onClosing(self):
        self.__form.destroy()
        self.__parent.Show()
        del self

    def Show(self):
        self.__LoadControls()
        self.__form.deiconify()
        self.__form.update()
