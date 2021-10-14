from os import name
import os
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox as MessageBox
from businessLogic.userManager import UserManager
from entites.user import User

from ui.appConfig import AppConfig
from ui.appStyles import AppStyles

class UserRegisterForm:

    #Propiedades para Anchor y Sticky
    #NW     N       NE
    #W    CENTER     E
    #SW     S       SE
    __userManager = UserManager()


    def __init__(self, parent) -> None:

        self.__parent = parent
        self.__form = Toplevel()

        self.setIcon()
        
        if AppConfig().IsThemeEnabled():
            AppStyles().ConfigureStyles(self.__form)

        #Tamaño
        # self.__form.resizable(0,0)#bloqueo horizontal y vertical

        #Titulo
        self.__form.title("Registro de Usuario")

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
        self.__frame.pack(anchor=NW, fill=X, padx=25, pady=15)

        #NAME
        self.__frameName = ttk.Frame(self.__frame)
        self.__frameName.pack(anchor=NW, fill=X, pady=3)
        self.__lblName = ttk.Label(self.__frameName, text="Nombre: ", anchor=E, width=20)
        self.__lblName.pack(side=LEFT)
        self.__txtName = ttk.Entry(self.__frameName, width=30)
        self.__txtName.pack(side=LEFT, fill=X, expand=1, padx=25)
        
        #LASTNAME
        self.__frameLastname = ttk.Frame(self.__frame)
        self.__frameLastname.pack(anchor=NW, fill=X, pady=3)
        self.__lblLastname = ttk.Label(self.__frameLastname, text="Apellido: ", anchor=E, width=20)
        self.__lblLastname.pack(side=LEFT)
        self.__txtLastname = ttk.Entry(self.__frameLastname, width=30)
        self.__txtLastname.pack(side=LEFT, fill=X, expand=1, padx=25)
        
        #EMAIL
        self.__frameEmail = ttk.Frame(self.__frame)
        self.__frameEmail.pack(anchor=NW, fill=X, pady=3)
        self.__lblEmail = ttk.Label(self.__frameEmail, text="Email: ", anchor=E, width=20)
        self.__lblEmail.pack(side=LEFT)
        self.__txtEmail = ttk.Entry(self.__frameEmail, width=30)
        self.__txtEmail.pack(side=LEFT, fill=X, expand=1, padx=25)
        
        #PASSWORD
        self.__framePassword = ttk.Frame(self.__frame)
        self.__framePassword.pack(anchor=NW, fill=X, pady=3)
        self.__lblPassword = ttk.Label(self.__framePassword, text="Contraseña: ", anchor=E, width=20)
        self.__lblPassword.pack(side=LEFT)
        self.__txtPassword = ttk.Entry(self.__framePassword, width=30)
        self.__txtPassword.pack(side=LEFT, fill=X, expand=1, padx=25)
        
        #CONFIRM PASSWORD
        self.__frameConfirmPass = ttk.Frame(self.__frame)
        self.__frameConfirmPass.pack(anchor=NW, fill=X, pady=3)
        self.__lblConfirmPass = ttk.Label(self.__frameConfirmPass, text="Confirmar contraseña: ", anchor=E, width=20)
        self.__lblConfirmPass.pack(side=LEFT)
        self.__txtConfirmPass = ttk.Entry(self.__frameConfirmPass, width=30)
        self.__txtConfirmPass.pack(side=LEFT, fill=X, expand=1, padx=25)
        
        #BUTTONS
        self.__frameButtons = ttk.Frame(self.__frame)
        self.__frameButtons.pack(side=TOP, pady=6)
        self.__btnCancel = ttk.Button(self.__frameButtons, width=15, text="Cancelar", command=self.btnCancel_Click)
        self.__btnCancel.pack(side=LEFT, padx=3)
        self.__btnSave = ttk.Button(self.__frameButtons, width=15, text="Guardar", command=self.btnSave_Click)
        self.__btnSave.pack(side=RIGHT)

        #Caputar evento de cierre
        self.__form.protocol("WM_DELETE_WINDOW", self.__onClosing)

        #Mostrar ventana hasta que se cierre
        self.__form.mainloop()

    def btnSave_Click(self):
        name = self.__txtName.get()
        lastName = self.__txtLastname.get()
        email = self.__txtEmail.get()
        password = self.__txtPassword.get().encode('utf8')
        passwordConfirm = self.__txtConfirmPass.get().encode('utf8')

        user = User(names=name, lastNames=lastName, email=email, password=password)
        count = self.__userManager.SignUp(user, passwordConfirm)
        
        if count >= 1:
            response = MessageBox.showinfo("Exito", "Ya estas registrado!")
            if(response==MessageBox.OK):
                self.__onClosing()
        else:
            MessageBox.showinfo("Error", "Discupa, ocurrió un problema y no te has podido registrar.")

    def btnCancel_Click(self):
        self.__onClosing()


    def setIcon(self):
        #Ruta absoluta
        rutaIcono = os.path.abspath("../notes.ico")
        if not os.path.isfile(rutaIcono):
            rutaIcono=os.path.abspath("./section22-TkinterMySql/notes.ico")

        #Icono del form
        self.__form.iconbitmap(rutaIcono)

    def __onClosing(self):
        self.__form.destroy()
        self.__parent.Show()
        del self
