
from tkinter import Tk
from tkinter.ttk import Style

from infrastructure.singleton import singleton

@singleton
class AppStyles:
    
    __style:Style = None

    def __init__(self):
        self.__style = Style()

    @classmethod
    def ConfigureStyles(cls, form = None):
        classInstance =cls()

        colors = {
                "bg": "white",
                "btnbg": "#f6f5f5",
                "btnfg": "#276678",
                "btnbg-active": "#d3e0ea",
                "btnfg-active": "#1687a7",
                "selectbg": "#657a9e",
                "selectfg": "#ffffff",
                "fontfg": "#282828",
            }

        styles = {
            "default-font" : ('Console', 12),
            "button-font" : ('Console', 11, 'bold')
        }

        #Form configures
        if form is not None:
            form.configure(bg=colors.get("bg"))

        #General Styles
        # cls.style.configure('.', bg=colors.get("bg"))

        #Frame Styles
        classInstance.__style.configure('TFrame', background=colors.get("bg"))

        #Label Styels
        classInstance.__style.configure('TLabel', background=colors.get("bg"))

        #Entry Styles
        classInstance.__style.map('TEntry', foreground=[("active", "black"), ("focus", colors.get("fontfg"))])

        #Button Styles
        classInstance.__style.configure('TButton', 
                            # font =  styles.get("button-font"),
                            borderwidth = '1', 
                            background=colors.get("btnbg"),
                            foreground=colors.get("btnfg"))
        classInstance.__style.map('TButton', foreground = [('active', '!disabled', colors.get("btnfg-active"))])
        classInstance.__style.map('TButton', background = [('active', colors.get("btnbg-active"))])

        # classInstance.__style.theme_create("appStyle", "default", 
        #     settings={
        #         ".": {
        #             "configure": {
        #                 "background": colors.get("bg"),
        #                 "troughcolor": colors.get("bg"),
        #                 "selectbackground": colors['selectbg'],
        #                 "selectforeground": colors['selectfg'],
        #                 "fieldbackground": colors.get("bg"),
        #                 "font": styles.get("default-font"),
        #                 "borderwidth": 1
        #             }
        #         },
        #         "TEntry": {
        #                     "configure": {
        #                         "height" :  35
        #                     }
        #                 },
        #         "TButton": {
        #                     "configure": {
        #                         "font" :  styles.get("button-font"),
        #                         "borderwidth" : '1', 
        #                         "background" : colors.get("btnbg"),
        #                         "foreground" : colors.get("btnfg")
        #                     },
        #                     "map": {
        #                         "foreground" : [('active', '!disabled', colors.get("btnfg-active"))],
        #                         "background" : [('active', colors.get("btnbg-active"))]
        #                     }
        #                     ,"layout": [
        #                         ('Button.button', {
        #                             'sticky': 'nswe', 
        #                             'children': [
        #                                 ('Button.focus', {
        #                                     'sticky': 'nswe', 
        #                                     'children': [
        #                                         ('Button.padding', {
        #                                             'sticky': 'nswe', 
        #                                             'children': [
        #                                                 ('Button.label', {
        #                                                     'sticky': 'nswe'
        #                                                     }
        #                                                 )]
        #                                             }
        #                                         )]
        #                                     }
        #                                 )]
        #                             }
        #                         )
        #                     ]
        #                 }
        #         })

        #classInstance.__style.theme_use("appStyle")

        return classInstance.__style
