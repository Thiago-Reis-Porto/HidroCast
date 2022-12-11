import customtkinter


class curve_frame(customtkinter.CTkFrame):
    def __init__(self, master, data, f_run, *args, lt='label title', fm=["linear"], **kwargs):
        super(curve_frame, self).__init__(master, *args, **kwargs)
        self.pack(fill='both', expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Title Frame
        frame_title = customtkinter.CTkFrame(self)
        frame_title.columnconfigure(list(range(5)), weight=1)
        frame_title.grid(row=0, column=0, sticky="ew")

        label_title = customtkinter.CTkLabel(frame_title,
                                             text=lt,
                                             text_font='Helvetica 12 bold')
        label_title.pack(pady=10)

     # Frame curve fit
        # left
        frame_CF = customtkinter.CTkFrame(self, fg_color="#2a2d2e")
        frame_CF.columnconfigure(0, weight=1)
        frame_CF.rowconfigure(1, weight=1)
        frame_CF.rowconfigure(list(range(2, 6)), weight=0)
        frame_CF.rowconfigure(list(range(7, 15)), weight=1)
        frame_CF.grid(row=1, column=0, sticky="nsew")

      #   label_VG = customtkinter.CTkLabel(frame_CF,
      #                                     text="Curve Fit:",
      #                                     text_font='Helvetica 10 bold')
      #   label_VG.grid(row=0, column=0)
        
        #--------------------------------------------------------------------------
        frame_menu = customtkinter.CTkFrame(frame_CF, height=30)
        #frame_menu.rowconfigure(list(range(0, 4)), weight=1)
        frame_menu.rowconfigure(list(range(2)), weight=1)
        frame_menu.grid(row=0, column=0, )#sticky="nsew")

        label_VG = customtkinter.CTkLabel(frame_menu,
                                           text="Curve Fit:",
                                           text_font='Helvetica 10 bold')
        label_VG.grid(row=0, column=0)

        # menu = customtkinter.CTkOptionMenu(frame_menu, 
        #                                    values=['d','c'], )
        #                                    #command = self.__change_table)
        # menu.grid(row=0, column=1, pady=10)
        #--------------------------------------------------------------------------

        f = customtkinter.CTkFrame(frame_CF, fg_color="white")
        f_pos = {'row': 1, 
                 'column': 0,
                 'sticky': "nsew",
                 'rowspan': 14,
                 'pady': 10,
                 'padx': 10}

        frame_CF.image_viz = f
        f.grid(**f_pos)

        # right
        label_depth = customtkinter.CTkLabel(frame_CF, text="Function")
        label_depth.grid(row=2, column=1, pady=1)
        menu_depth = customtkinter.CTkOptionMenu(frame_CF,
                                                 values=fm,
                                                 width=70)
        menu_depth.grid(row=3, column=1)

        buttom_run = customtkinter.CTkButton(master=frame_CF,
                                             text="RUN",
                                             command=lambda: f_run(frame_CF, data, **f_pos),
                                             width=100)

        buttom_run.grid(row=4, column=1, padx=10, pady=10)
