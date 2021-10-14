import os
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox as MessageBox

from businessLogic.userManager import UserManager
from ui.appConfig import AppConfig
from ui.appStyles import AppStyles
from ui.mainForm import MainForm
from ui.userRegisterForm import UserRegisterForm

class UserLoginForm():

    #Propiedades para Anchor y Sticky
    #NW     N       NE
    #W    CENTER     E
    #SW     S       SE

    manager = UserManager()


    def __init__(self):
        self.__form = Tk()
        super().__init__()

        self.setIcon()
        
        if AppConfig().IsThemeEnabled():
            AppStyles().ConfigureStyles(self.__form)

        #Tamaño
        self.__form.resizable(0,0)#bloqueo horizontal y vertical

        #Titulo
        self.__form.title("Quick Notes - Login")
        # self.configure(bg="white", border=0)
        
        #Ubico el formulario en el centro de la pantalla
        self.__form.__width = 350
        self.__form.__height = 150
        screen_width = self.__form.winfo_screenwidth()
        screen_height = self.__form.winfo_screenheight()
        x = (screen_width/2) - (self.__form.__width/2)
        y = (screen_height/2) - (self.__form.__height/2)
        self.__form.geometry("%dx%d+%d+%d" % (self.__form.__width, self.__form.__height, x, y))
        
        #Frame contenedor
        self.__frame = ttk.Frame(self.__form)
        self.__frame.pack(anchor=NW, fill=X, pady=15)

        #Email
        self.__svEmail = StringVar()
        self.__svEmail.trace_add("write", self.txtEmail_TextChanged)
        self.__frameEmail = ttk.Frame(self.__frame)
        self.__frameEmail.pack(anchor=NW, fill=X, padx=25, pady=5)
        self.__lblEmail = ttk.Label(self.__frameEmail, text="Email: ", anchor=E
                              , width=12)
        self.__lblEmail.pack(side=LEFT)
        self.__txtEmail = ttk.Entry(self.__frameEmail, textvariable=self.__svEmail)
        self.__txtEmail.pack(side=LEFT, fill=X, expand=1)
        # self.__combo = Combobox(self.__frameEmail, state="readonly")
        # self.__combo["values"] = ["Python", "C", "C++", "Java"]
        # self.__combo.pack(side=LEFT, fill=X, expand=1)

        #Password
        self.__svPassword = StringVar()
        self.__svPassword.trace_add("write", self.txtPassword_TextChanged)
        self.__framePassword = ttk.Frame(self.__frame)
        self.__framePassword.pack(anchor=NW, fill=X, padx=25)
        self.__lblPassword = ttk.Label(self.__framePassword, text="Contraseña: ", anchor=E
                                 , width=12)
        self.__lblPassword.pack(side=LEFT)
        self.__txtPassword = ttk.Entry(self.__framePassword, textvariable=self.__svPassword, show="*")
        self.__txtPassword.pack(side=LEFT, fill=X, expand=1)

        #Buttons
        self.__frameButtons = ttk.Frame(self.__frame)
        self.__frameButtons.pack(anchor=NW, fill=X, padx=25, pady=5)
        self.__btnLogin = ttk.Button(self.__frameButtons, text="Login",command=self.btnLogin_Click
                               , width=15,state=DISABLED)
        self.__btnLogin.pack(side=RIGHT)
        self.__btnRegistro = ttk.Button(self.__frameButtons, text="Nuevo usuario", command=self.btnRegistro_Click)
        self.__btnRegistro.pack(anchor=E, padx=6)
        
        self.__form.bind('<Return>', self.btnLogin_Click)

        self.__LoadLoginConfig()

        #Mostrar ventana hasta que se cierre
        self.__form.mainloop()
    
    def txtEmail_TextChanged(self, *args):
        self.__EnsureEnableLogin()

    def txtPassword_TextChanged(self, *args):
        self.__EnsureEnableLogin()
        
    def btnLogin_Click(self, event):
        email = self.__svEmail.get()
        password = self.__svPassword.get()
        self.__DoLogin(email, password)
            
    def btnRegistro_Click(self):
        self.__form.withdraw()
        UserRegisterForm(self)


    def setIcon(self):
        #Ruta absoluta
        rutaIcono = os.path.abspath("./notes.ico")
        if not os.path.isfile(rutaIcono):
            rutaIcono=os.path.abspath("./section22-TkinterMySql/notes.ico")

        #Icono del form
        self.__form.iconbitmap(rutaIcono)

    def __LoadLoginConfig(self):
        loginConfig = AppConfig().GetLoginConfig()
        if loginConfig is not None:
            self.__DoLogin(loginConfig[0],loginConfig[1])

    def __DoLogin(self, email, password):
        try:
            self.__LoggedUser = self.manager.Login(email, password.encode('utf8'))

            if self.__LoggedUser is not None:
                self.__ClearForm()
                self.__form.withdraw()
                MainForm(self, self.__LoggedUser)
            else:
                MessageBox.showerror("Error", "El usuario y contraseña ingresados no son validos!")
        except Exception:
            MessageBox.showerror("Error", "Oops, ocurrió un error no esperado.")

    def Quit(self):
        self.__form.quit()

    def Show(self):
        self.__form.deiconify()
        self.__form.update()

    def __EnsureEnableLogin(self):
        email = self.__svEmail.get()
        password = self.__svPassword.get()
        if not (email.strip() and password.strip()):
            self.__btnLogin["state"] = DISABLED
            self.__form.unbind('<Return>')
        else:
            self.__btnLogin["state"] = NORMAL
            self.__form.bind('<Return>', self.btnLogin_Click)


    def __ClearForm(self):
        self.__svEmail.set("")
        self.__svPassword.set("")


        