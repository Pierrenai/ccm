try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
    from tkinter.ttk import Treeview
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2

import sqlite3
import os

MaterialsList = []
SpecsList = []
ProvidersList = []


def set_providers():
    providers = "SELECT NAME FROM PROVIDERS;"

    connection = sqlite3.connect("ccm.db")
    cursor = connection.cursor()

    cursor.execute(providers)
    results = cursor.fetchall()

    for row in results:
        print(row)
        ProvidersList.append(format(*row))

    cursor.close()
    connection.close()

    return results[0][0]


set_providers()


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("CCM")
        self.geometry("800x480")
        self.minsize(750, 480)
        self.config(background='BLUE')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, CCMPage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Quitter", command=self.quit)
        menu_bar.add_cascade(label="Fichier", menu=file_menu)

        self.config(menu=menu_bar)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Certificat Conformité Matière", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="CCM",
                            command=lambda: controller.show_frame("CCMPage"))
        button2 = tk.Button(self, text="OPTIONS",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class CCMPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def cleartext():
            Info_Label['text'] = ""

        def openfile():
            ncom = ncom_entry.get()

            providerquery = "SELECT PROVIDER FROM CCM WHERE NCOM='" + ncom + "';"

            connection = sqlite3.connect("ccm.db")
            cursor = connection.cursor()

            cursor.execute(providerquery)
            provider = format(*cursor.fetchone())
            print(provider)

            cursor.close()
            connection.close()

            path = os.path.abspath(os.getcwd())
            path = os.path.join(path, 'CCM', provider)

            if not os.path.exists(path):
                os.mkdir(path)
                print("Directory ", path, " Created ")
            else:
                print("Directory ", path, " already exists")

            path = os.path.abspath(os.getcwd())
            path = os.path.join(path, 'CCM', provider, ncom)

            if not os.path.exists(path):
                os.mkdir(path)
                print("Directory ", path, " Created ")
            else:
                print("Directory ", path, " already exists")

            os.startfile(path)

            ncom_entry.delete(0, 'end')

        def get_all():
            for i in tree.get_children():
                tree.delete(i)
            query = "SELECT * FROM CCM;"

            connection = sqlite3.connect("ccm.db")
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                print(row)

                tree.insert("", tk.END, values=row)

            cursor.close()
            connection.close()

            cleartext()
            return results[0][0]

        def checkifexist(ncom):
            query = "SELECT * FROM CCM WHERE NCOM='" + ncom + "'; "

            connection = sqlite3.connect("ccm.db")
            cursor = connection.cursor()
            cursor.execute(query)
            results = format(cursor.fetchall())
            print(results)

            if results == "[]":
                return False
            else:
                return True

            cursor.close()
            connection.close()

        def add_ccm():
            ncom = ncom_entry.get()
            provider = providers_variable.get()

            cleartext()

            if ncom:

                if bool(checkifexist(ncom)):
                    Info_Label['text']= "Existe déjà"

                else:
                    query = "INSERT INTO CCM (NCOM, PROVIDER) VALUES ('" + ncom + "', '" + provider + "'); "

                    connection = sqlite3.connect("ccm.db")
                    cursor = connection.cursor()
                    cursor.execute(query)

                    connection.commit()
                    cursor.close()
                    connection.close()

                openfile()
                ncom_entry.delete(0, 'end')

            else:
                Info_Label['text']="Entrer un numéro de certificat"

        def remove_ccm():
            ncom = ncom_entry.get()

            query = "DELETE FROM CCM WHERE NCOM='" + ncom + "'; "

            connection = sqlite3.connect("ccm.db")
            cursor = connection.cursor()
            cursor.execute(query)

            connection.commit()
            cursor.close()
            connection.close()

            ncom_entry.delete(0, 'end')
            cleartext()

        label = tk.Label(self, text="CCM", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        tree = Treeview(self, column=("c1", "c2", "c3"),
                        show='headings')

        tree.column("#1", anchor=tk.CENTER, minwidth=10, width=50, stretch=tk.NO)

        tree.heading("#1", text="ID")

        tree.column("#2", anchor=tk.CENTER, minwidth=10, width=100, stretch=tk.NO)

        tree.heading("#2", text="N COMMANDE")

        tree.column("#3", anchor=tk.CENTER, minwidth=10, width=150, stretch=tk.NO)

        tree.heading("#3", text="FOURNISSEUR")

        tree.pack()

        display_button = tk.Button(self, text="Afficher CCM", command=get_all)
        display_button.pack()

        frame = tk.Frame(self)

        ncom_Label = tk.Label(frame, text="N COMMANDE", font=("Courrier", 20), bg='#D3D3D3', fg='white', width=20)
        ncom_Label.grid(row=0, column=0)

        provider_Label = tk.Label(frame, text="FOURNISSEUR", font=("Courrier", 20), bg='#D3D3D3', fg='white', width=20)
        provider_Label.grid(row=0, column=1)

        ncom_entry = tk.Entry(frame, text="", font=("Courrier", 20), bg='#D3D3D3', fg='white', width=20)
        ncom_entry.grid(row=1, column=0)

        providers_variable = tk.StringVar(frame)
        providers_variable.set(ProvidersList[0])

        opt = tk.OptionMenu(frame, providers_variable, *ProvidersList)
        opt.config(width=20, font=('Helvetica', 12))
        opt.grid(row=1, column=1)

        add_button = tk.Button(frame, text="+", command=add_ccm)
        add_button.grid(row=1, column=9)

        remove_button = tk.Button(frame, text="-", command=remove_ccm)
        remove_button.grid(row=1, column=10)

        openfile_ccm_button = tk.Button(frame, text="Ouvrir fichier", command=openfile)
        openfile_ccm_button.grid(row=2, column=0)

        frame.pack()

        button = tk.Button(self, text="MENU",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        Info_Label = tk.Label(self, text="", font=("Courrier", 20), fg='RED', width=40)
        Info_Label.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="SETTINGS", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        def add_providers():
            string = string_entry.get()

            query = "INSERT INTO PROVIDERS (NAME) VALUES ('" + string + "');"

            connection = sqlite3.connect("ccm.db")
            cursor = connection.cursor()
            cursor.execute(query)

            connection.commit()
            cursor.close()
            connection.close()

            string_entry.delete(0, 'end')

        def remove_providers():
            string = string_entry.get()

            query = "DELETE FROM PROVIDERS WHERE NAME='" + string + "'"

            connection = sqlite3.connect("ccm.db")
            cursor = connection.cursor()
            cursor.execute(query)

            connection.commit()
            cursor.close()
            connection.close()

            string_entry.delete(0, 'end')

        string_entry = tk.Entry(self, text="", font=("Courrier", 40), bg='#D3D3D3', fg='white')
        string_entry.pack()

        frame = tk.Frame(self)

        providers_variable = tk.StringVar(frame)
        providers_variable.set(ProvidersList[0])

        opt = tk.OptionMenu(frame, providers_variable, *ProvidersList)
        opt.config(width=20, font=('Helvetica', 12))
        opt.grid(row=0, column=2)

        providers_add_button = tk.Button(frame, text="AJOUTER FOURNISSEUR", command=add_providers)
        providers_add_button.grid(row=1, column=2)

        providers_remove_button = tk.Button(frame, text="SUPPRIMER FOURNISSEUR", command=remove_providers)
        providers_remove_button.grid(row=2, column=2)

        frame.pack()

        button = tk.Button(self, text="MENU",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
