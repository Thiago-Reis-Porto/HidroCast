import customtkinter
from utils import only_numbers
from utils import browse_files, browse_files_2
from pandastable import Table

def wraper_load(label, data, key):
    browse_files(label, data, key)
    print(key)
    data["DEPTHS"] = data[key].columns
    data["TIME"] = data[key].index
    if key == "PSI M":
        data[key] = data[key].abs()

def create_view_window(root, data, key):
    if data[key] is None:
        return
    window = customtkinter.CTkToplevel(root)
    window.geometry("600x400")
    window.title(key)
    table = Table(window, dataframe=data[key], editable=False)
    table.show()

def set_data_frame(notebook):
    data_frame = customtkinter.CTkFrame(notebook)
    notebook.data_frame = data_frame
    data_frame.pack(fill="both", expand=True)
    data = notebook.root.data
    # grid 24x3
    data_frame.grid_columnconfigure(0, weight=1)
    data_frame.grid_columnconfigure(2, weight=1)

    data_frame.grid_rowconfigure([i for i in range(26)], weight=1)
    data_frame.grid_rowconfigure(26, minsize=20)
    # data_frame.grid_rowconfigure(5, minsize=10)
    # data_frame.grid_rowconfigure(8, minsize=10)
    # data_frame.grid_rowconfigure(11, minsize=10)
    # data_frame.grid_rowconfigure(14, minsize=10)
    # data_frame.grid_rowconfigure(17, minsize=10)
    # data_frame.grid_rowconfigure(20, minsize=10)

    # -----------TENSIOMETER-----------
    key_1 = "TENSIOMETER"
    label_tensio = customtkinter.CTkLabel(
        data_frame, text=key_1, text_font="Helvetica 10 bold")
    label_tensio.grid(row=0, column=1, pady=10)

    label_tensio_file = customtkinter.CTkLabel(data_frame, text="No File")
    label_tensio_file.grid(row=1, column=2)

    button_tensio_load = customtkinter.CTkButton(master=data_frame,
                                                 text="LOAD",
                                                 command=lambda: wraper_load(label_tensio_file,
                                                                              data,
                                                                              key_1),
                                                 width=60)
    button_tensio_load.grid(row=1, column=0)

    button_tensio_view = customtkinter.CTkButton(master=data_frame,
                                                 text="VIEW",
                                                 command=lambda: create_view_window(data_frame,
                                                                                    data,
                                                                                    key_1),
                                                 width=60)
    button_tensio_view.grid(row=1, column=1)

    # -----------THETAS PHI-----------
    key_2 = "THETAS PHI"
    label_theta_phi = customtkinter.CTkLabel(
        data_frame, text=key_2, text_font="Helvetica 10 bold")
    label_theta_phi.grid(row=3, column=1, pady=10)

    label_thetas_phi_file = customtkinter.CTkLabel(data_frame, text="No File")
    label_thetas_phi_file.grid(row=4, column=2)
    button_theta_phi = customtkinter.CTkButton(master=data_frame,
                                               text="LOAD",
                                               command=lambda: browse_files(label_thetas_phi_file,
                                                                            data,
                                                                            key_2),
                                               width=60)
    button_theta_phi.grid(row=4, column=0)

    button_psi_m_view = customtkinter.CTkButton(master=data_frame,
                                                text="VIEW",
                                                command=lambda: create_view_window(data_frame,
                                                                                    data,
                                                                                    key_2),
                                                width=60)
    button_psi_m_view.grid(row=4, column=1)

    # -----------PSI M-----------
    key_3 = "PSI M"
    label_psi_m = customtkinter.CTkLabel(
        data_frame, text=key_3, text_font="Helvetica 10 bold")
    label_psi_m.grid(row=6, column=1, pady=10)

    label_psi_m_file = customtkinter.CTkLabel(data_frame, text="No File")
    label_psi_m_file.grid(row=7, column=2)

    button_psi_m_load = customtkinter.CTkButton(master=data_frame,
                                                text="LOAD",
                                                command=lambda: wraper_load(label_psi_m_file,
                                                                             data,
                                                                             key_3),
                                                width=60
                                                )
    button_psi_m_load.grid(row=7, column=0)

    button_psi_m_view = customtkinter.CTkButton(master=data_frame,
                                                text="VIEW",
                                                command=lambda: create_view_window(data_frame,
                                                                                    data,
                                                                                    key_3),
                                                width=60)
    button_psi_m_view.grid(row=7, column=1)

    # -----------THETAS TIME-----------
    key_4= "THETAS TIME"
    label_theta_time = customtkinter.CTkLabel(
        data_frame, text=key_4, text_font="Helvetica 10 bold")
    label_theta_time.grid(row=9, column=1, pady=10)

    label_theta_time_file = customtkinter.CTkLabel(data_frame, text="No File")
    label_theta_time_file.grid(row=10, column=2)
    button_theta_time = customtkinter.CTkButton(master=data_frame,
                                                text="LOAD",
                                                command=lambda: wraper_load(label_theta_time_file,
                                                                             data,
                                                                             key_4),
                                                width=60)
    button_theta_time.grid(row=10, column=0)

    button_theta_time_view = customtkinter.CTkButton(master=data_frame,
                                                     text="VIEW",
                                                     command=lambda: create_view_window(data_frame,
                                                                                    data,
                                                                                    key_4),
                                                     width=60)
    button_theta_time_view.grid(row=10, column=1)



    # -----------THETA 0-----------
    key_7 = "THETA 0"
    label_theta_s = customtkinter.CTkLabel(
        data_frame, text=key_7, text_font="Helvetica 10 bold")
    label_theta_s.grid(row=12, column=1, pady=10)

    label_theta_s_file = customtkinter.CTkLabel(data_frame, text="No File")
    label_theta_s_file.grid(row=13, column=2)

    button_theta_s = customtkinter.CTkButton(master=data_frame,
                                             text="LOAD",
                                             command=lambda: browse_files_2(label_theta_s_file,
                                                                          data,
                                                                          key_7),
                                             width=60)
    button_theta_s.grid(row=13, column=0)

    button_theta_s_view = customtkinter.CTkButton(master=data_frame,
                                                  text="VIEW",
                                                  command=lambda: create_view_window(data_frame,
                                                                                    data,
                                                                                    key_7),
                                                  width=60)
    button_theta_s_view.grid(row=13, column=1)

    # # -----------THETA 0-----------
    # key_8 = "THETA 0"
    # label_theta_0 = customtkinter.CTkLabel(
    #     data_frame, text=key_8, text_font="Helvetica 10 bold")
    # label_theta_0.grid(row=21, column=1, pady=10)

    # label_theta_0_file = customtkinter.CTkLabel(data_frame, text="No File")
    # label_theta_0_file.grid(row=22, column=2)

    # button_theta_0 = customtkinter.CTkButton(master=data_frame,
    #                                          text="LOAD",
    #                                          command=lambda: browse_files_2(label_theta_s_file,
    #                                                                       data,
    #                                                                       key_8),
    #                                          width=60
    #                                          )
    # button_theta_0.grid(row=22, column=0)

    # button_theta_0_view = customtkinter.CTkButton(master=data_frame,
    #                                               text="VIEW",
    #                                               command=lambda: print(
    #                                                   data[key_8]),
    #                                               width=60
    #                                               )
    # button_theta_0_view.grid(row=22, column=1)

    # -----------DELTA-----------
    key_9 = "DELTA"
    label_delta = customtkinter.CTkLabel(
        data_frame, text=key_9, text_font="Helvetica 10 bold")
    label_delta.grid(row=21, column=1, pady=10)

    validation = notebook.register(only_numbers)
    sv = customtkinter.StringVar()
    sv.trace("w", lambda name, index, mode,
             sv=sv: data.update({key_9: int(sv.get())}))

    t = customtkinter.CTkEntry(data_frame, validate="key", validatecommand=(
        validation, "%S"), textvariable=sv)
    t.grid(row=22, column=1)

    notebook.add(data_frame, text="Data")
    return notebook
