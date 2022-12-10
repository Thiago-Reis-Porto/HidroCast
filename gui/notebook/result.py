import customtkinter

def set_result(notebook, method):
    try:
        if notebook.results[method]:
            result_frame = notebook.results[method]
            notebook.result_frame = result_frame
            result_frame.pack(fill="both", expand=True)
            notebook.add(result_frame, text="Result")
            notebook.tab_list.append(result_frame)
    except:
        result_frame = customtkinter.CTkFrame(notebook)
        notebook.result_frame = result_frame
        result_frame.pack(fill="both", expand=True)
        notebook.add(result_frame, text="Result")
        notebook.tab_list.append(result_frame)
        notebook.results[method] = result_frame
    return notebook
