import tkinter

class ScrollableImage(tkinter.Frame):
    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        sw = kw.pop('scrollbarwidth', 10)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self.cnvs = tkinter.Canvas(self, highlightthickness=0, **kw)
        self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
        # Vertical and Horizontal scrollbars
        self.v_scroll = tkinter.Scrollbar(self, orient='vertical', width=sw)
        self.h_scroll = tkinter.Scrollbar(self, orient='horizontal', width=sw)
        # Grid and configure weight.
        self.cnvs.grid(row=0, column=0,  sticky='nsew', padx=1, pady=1)
        self.h_scroll.grid(row=1, column=0, sticky='ew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Set the scrollbars to the canvas
        self.cnvs.config(xscrollcommand=self.h_scroll.set, 
                           yscrollcommand=self.v_scroll.set)
        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.cnvs.yview)
        self.h_scroll.config(command=self.cnvs.xview)
        # Assign the region to be scrolled 
        self.cnvs.config(scrollregion=self.cnvs.bbox('all'))
        self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)

    def mouse_scroll(self, evt):
        if evt.state == 0 :
            self.cnvs.yview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.cnvs.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
        if evt.state == 1:
            self.cnvs.xview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.cnvs.xview_scroll(int(-1*(evt.delta/120)), 'units') # For windows

def mouse_scroll(canvas, evt):
    if evt.state == 0 :
        canvas.yview_scroll(-1*(evt.delta), 'units') # For MacOS
        canvas.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
    if evt.state == 1:
        canvas.xview_scroll(-1*(evt.delta), 'units') # For MacOS
        canvas.xview_scroll(int(-1*(evt.delta/120)), 'units') # For windows

def scrollable_canvas(canvas, sw):

        # Vertical and Horizontal scrollbars
        canvas.v_scroll = tkinter.Scrollbar(canvas, orient='vertical', width=sw)
        canvas.h_scroll = tkinter.Scrollbar(canvas, orient='horizontal', width=sw)
        # Grid and configure weight.
        canvas.grid(row=0, column=0,  sticky='nsew')
        canvas.h_scroll.grid(row=1, column=0, sticky='ew')
        canvas.v_scroll.grid(row=0, column=1, sticky='ns')
        canvas.rowconfigure(0, weight=1)
        canvas.columnconfigure(0, weight=1)
        # Set the scrollbars to the canvas
        canvas.config(xscrollcommand=canvas.h_scroll.set, 
                           yscrollcommand=canvas.v_scroll.set)
        # Set canvas view to the scrollbars
        canvas.v_scroll.config(command=canvas.yview)
        canvas.h_scroll.config(command=canvas.xview)
        # Assign the region to be scrolled 
        canvas.config(scrollregion=canvas.bbox('all'))
        canvas.bind_class(canvas, "<MouseWheel>", mouse_scroll)



