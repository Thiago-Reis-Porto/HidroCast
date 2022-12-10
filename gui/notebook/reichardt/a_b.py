from gui.notebook.hillel.curve_fit_tab import curve_frame
from methods.reichardt import pipeline_a_b

def set_a_b(notebook):
    try:
        if notebook.a_b_frame:
            a_b_frame = notebook.a_b_frame
            notebook.add(a_b_frame, text="a b")
            notebook.tab_list.append(a_b_frame)
    except:
        a_b_frame = curve_frame(notebook,
                                notebook.root.data,
                                pipeline_a_b,
                                lt=r"θ x Mean(θ)")
                                
        notebook.a_b_frame = a_b_frame
        notebook.add(a_b_frame, text="a b")
        notebook.tab_list.append(a_b_frame)
        
    return notebook