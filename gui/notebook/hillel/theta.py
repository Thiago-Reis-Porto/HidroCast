import customtkinter
from methods.hillel.theta_time import run_theta_time_pipeline
from gui.notebook.hillel.curve_fit_tab import curve_frame

def set_theta(notebook):
    
    try:
        if notebook.theta_frame:
            theta_frame = notebook.theta_frame
            notebook.add(theta_frame, text="θ x Time")
            notebook.tab_list.append(theta_frame)
            
    except:
        theta_frame = curve_frame(notebook,
                                notebook.root.data,
                                run_theta_time_pipeline,
                                lt="θ x TIME")
        notebook.theta_frame = theta_frame
        notebook.add(theta_frame, text="θ x Time")
        notebook.tab_list.append(theta_frame)

    return notebook
