from tkinter import S
import customtkinter
from methods.hillel.tensio_psi_m import set_psiM_from_tensio
from methods.hillel.tensio_psi_m import get_VG_params_set_theta_time
from gui.notebook.hillel.curve_fit_tab import curve_frame
# def set_psi_m_vg(notebook):

#     e_f_frame = curve_frame(notebook,
#                               notebook.root.data,
#                               pipeline_e_f,
#                               lt=r"θ x Mean(θ)")
                              
#     notebook.e_f_frame = e_f_frame
#     notebook.add(e_f_frame, text="e f")
#     notebook.tab_list.append(e_f_frame)
#     return notebook
"""
def set_psi_m_vg(notebook):
    psi_m_vg_frame = customtkinter.CTkFrame(notebook)
    notebook.psi_m_vg_frame = psi_m_vg_frame
    psi_m_vg_frame.pack(fill="both", expand=True)
    psi_m_vg_frame.columnconfigure(0, weight=1)
    psi_m_vg_frame.rowconfigure(1, weight=1)
    data = notebook.root.data
    # 1st Frame
    frame_psi = customtkinter.CTkFrame(psi_m_vg_frame)
    frame_psi.columnconfigure(list(range(5)), weight=1)
    frame_psi.grid(row=0, column=0, sticky="ew")

    label_to_psi = customtkinter.CTkLabel(frame_psi,
                                          text="Tensiometer to Ψm:",
                                          text_font="Helvetica 10 bold"
                                          )
    label_to_psi.grid(row=0, column=1)

    button_convert = customtkinter.CTkButton(master=frame_psi,
                                             text="CONVERT",
                                             command=lambda: set_psiM_from_tensio(data),
                                             width=60
                                             )
    button_convert.grid(row=0, column=2, pady=10)

    button_psi_view = customtkinter.CTkButton(master=frame_psi,
                                              text="VIEW",
                                              command=lambda: print(data["PSI M"]),
                                              width=60
                                              )
    button_psi_view.grid(row=0, column=3)

    # 2nd Frame
    # left
    frame_VG = customtkinter.CTkFrame(psi_m_vg_frame, fg_color="#2a2d2e")
    frame_VG.columnconfigure(0, weight=1)
    frame_VG.rowconfigure(list(range(1, 5)), weight=1)
    frame_VG.rowconfigure(list(range(2, 4)), weight=0)
    frame_VG.grid(row=1, column=0, sticky="nsew")

    label_VG = customtkinter.CTkLabel(frame_VG,
                                      text="Van Genutchen Parameters curve fit",
                                      text_font="Helvetica 10 bold"
                                      )
    label_VG.grid(row=0, column=0, pady=10)
    
    f = customtkinter.CTkFrame(frame_VG, fg_color="white")
    f_pos = {'row':1, 'column':0, 'sticky':"nsew", 'rowspan':4, 'pady':10, 'padx':10}
    frame_VG.image_viz = f
    #f.grid(row=1, column=0, sticky="nsew", rowspan=4, pady=10, padx=10)
    f.grid(**f_pos)
    # right
    switch_theta_s = customtkinter.CTkSwitch(frame_VG, text="θs as Input")
    switch_theta_s.grid(row=2, column=1, padx=10)

    buttom_run = customtkinter.CTkButton(master=frame_VG,
                                         text="RUN",
                                         command=lambda: get_VG_params_set_theta_time(data, frame_VG, **f_pos),
                                         width=100
                                         )
    buttom_run.grid(row=3, column=1, padx=10, pady=10)
    notebook.add(psi_m_vg_frame, text="Ψm - VG")
    notebook.tab_list.append(psi_m_vg_frame)
    return notebook"""