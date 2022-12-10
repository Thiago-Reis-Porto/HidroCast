from gui.notebook.hillel.curve_fit_tab import curve_frame
from methods.libard import pipeline_a

def set_a(notebook):
    try:
        if notebook.a_frame:
            a_frame = notebook.a_frame
            notebook.add(a_frame, text="a")
            notebook.tab_list.append(a_frame)
    except:
        a_frame = curve_frame(notebook,
                                notebook.root.data,
                                pipeline_a,
                                lt=r"θ x Mean(θ)")
                                
        notebook.a_frame = a_frame
        notebook.add(a_frame, text="a")
        notebook.tab_list.append(a_frame)
        
    return notebook

    