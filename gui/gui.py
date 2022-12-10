import tkinter
import customtkinter
from pandastable import Table
from gui.notebook.data import *
from gui.notebook.method_handler import set_method
from utils import data, get_tables_list
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

#GTK 3
class App(customtkinter.CTk):

    WIDTH = 1024
    HEIGHT = 576
    METHODS = ["Hillel et al. (1972)", 
               "Libardi et al. (1980)",
               "Reichardt et al. (2004)"]

    def __init__(self):
        super().__init__()

        self.title("HidroCast")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.data = data
        # ============ create three frames ============

        # configure grid layout (1x3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_center = customtkinter.CTkFrame(master=self)
        self.frame_center.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=2, sticky="nswe", padx=10, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
      #  self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_app_name = customtkinter.CTkLabel(master=self.frame_left,
                                              text="HidroCast",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_app_name.grid(row=1, column=0, pady=10, padx=10)

        self.button_open_p = customtkinter.CTkButton(master=self.frame_left,
                                                text="Open Project",
                                                command=self.button_event)
        self.button_open_p.grid(row=2, column=0, pady=10, padx=20)

        self.button_save_p = customtkinter.CTkButton(master=self.frame_left,
                                                text="Save Project",
                                                command=self.button_event)
        self.button_save_p.grid(row=3, column=0, pady=10, padx=20)

        self.button_help = customtkinter.CTkButton(master=self.frame_left,
                                                text="Help",
                                                command=self.button_event)
        self.button_help.grid(row=4, column=0, pady=10, padx=20)

        #Method def
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Method Selection:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")
        self.method_menu = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=self.METHODS,
                                                        command=self.__set_method_wraper)
        self.method_menu.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_center ============
        # configure grid layout (1x1)
        self.frame_center.rowconfigure(0, weight=1)
        self.frame_center.columnconfigure(0, weight=1)
        note = tkinter.ttk.Notebook(self.frame_center)      
        note.grid(column=0, row=0, sticky="nswe", padx=10, pady=10)
        note.root = self
        note = set_data_frame(note)
        note.tab_list = []
        note.actual_method = None
        note.results = {}
        note = set_method("Hillel et al. (1972)", note)                  
        self.note = note

        # ============ frame_right ============
        self.frame_right.rowconfigure([3,4,5,10], weight=1)

        button_home = customtkinter.CTkButton(self.frame_right, 
                                              text='VG',
                                              width=90)
        button_home.grid(row=0, pady=20)

        button_tables = customtkinter.CTkButton(self.frame_right, 
                                                text ='Tables',
                                                width =90,
                                                command = self.create_table_window) 
        button_tables.grid(row=1)

        button_plots = customtkinter.CTkButton(self.frame_right, 
                                                text='Plots',
                                                width=90)
        button_plots.grid(row=2, pady=20)


        label_depth = customtkinter.CTkLabel(self.frame_right, text="Depth unit")
        label_depth.grid(row=6,)
        
        menu_depth = customtkinter.CTkOptionMenu(self.frame_right, 
                                                 values=['cm'],
                                                 width=70)
        menu_depth.set('cm')
        menu_depth.grid(row=7)

        label_time = customtkinter.CTkLabel(self.frame_right, text="Time unit")
        label_time.grid(row=8)
        menu_time = customtkinter.CTkOptionMenu(self.frame_right, 
                                                values=['days'],
                                                width=70)
        menu_time.grid(row=9)
        menu_time.set('days')

       
        self.method_menu.set(self.METHODS[0])
 
    def __set_method_wraper(self, m):
        set_method(m, self.note)

    def __change_table(self, key):
        df = data[key].reset_index()
        t = self.table
        t.model.df = df
        t.redraw()
    
    def create_table_window(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("600x400")

        l = get_tables_list(data)

        menu = customtkinter.CTkOptionMenu(window, 
                                                values=l, 
                                                command = self.__change_table)
        menu.pack(fill='x')

        frame = customtkinter.CTkFrame(window)
        frame.pack(expand=True, fill='both')
        table = Table(frame, editable=False)
        self.table = table
        if l: 
            table.model.df = data[l[0]]
            table.show()
        else:
            menu.set('')
    def button_event(self):
        print("Button pressed")

    def on_closing(self, event=0):
        self.quit() 
        #self.destroy()




