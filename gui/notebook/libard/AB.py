from gui.notebook.hillel.curve_fit_tab import curve_frame
from methods.libard import pipeline_A_B

def set_AB(notebook):
    try:
        if notebook.a_b_frame:
            AB_frame = notebook.a_b_frame
            notebook.add(AB_frame, text="A B")
            notebook.tab_list.append(AB_frame)

    except:
        AB_frame = curve_frame(notebook,
                                notebook.root.data,
                                pipeline_A_B,
                                lt=r"\theta x \theta^_")
                                
        notebook.a_b_frame = AB_frame
        notebook.add(AB_frame, text="A B")
        notebook.tab_list.append(AB_frame)
        
    return notebook

    