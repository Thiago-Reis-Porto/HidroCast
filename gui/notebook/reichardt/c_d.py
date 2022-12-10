from gui.notebook.hillel.curve_fit_tab import curve_frame
from methods.reichardt import pipeline_c_d

def set_c_d(notebook):
    try:
        if notebook.c_d_frame:
            c_d_frame = notebook.c_d_frame
            notebook.add(c_d_frame, text="c d")
            notebook.tab_list.append(c_d_frame)
    except:
        c_d_frame = curve_frame(notebook,
                                notebook.root.data,
                                pipeline_c_d,
                                lt=r"θ x Mean(θ)")
                                
        notebook.c_d_frame = c_d_frame
        notebook.add(c_d_frame, text="c d")
        notebook.tab_list.append(c_d_frame)

    return notebook