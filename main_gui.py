"""

MAIN GUI: main Python code to create the GUI for TLoD TMD Converter

Copyright (C) 2023 DooMMetaL
"""

from tkinter import INSERT, CENTER, END, Canvas, Tk, Button, Frame, Text, LabelFrame, Label, messagebox, Scrollbar
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image
import webbrowser
import tlod_tmd_converter

class TCWindow(Frame):
    # Constructor

    def __init__(self, master=None, width=int, height=int):
        super().__init__(master, width=width, height=height)
        self.master = master
        self.pack()
        self.create_widget(width_mainframe=width, height_mainframe=height)
    
    def create_widget(self, width_mainframe=int, height_mainframe=int):
        #### Creation of widgets ####
        # Buttons - Labels - Frame - Text [Text Box Output]
        ## Image
        self.image_filename = "Resources/Ruff_GUI.png"
        self.open_image = Image.open(self.image_filename)
        self.x_y_values = self.resize_window(width_mainframe_change=width_mainframe, height_mainframe_change=height_mainframe)
        self.resize_image = self.open_image.resize(self.x_y_values, Image.Resampling.LANCZOS)
        self.image_background = ImageTk.PhotoImage(image=self.resize_image)
        ## Canvas (Background image)
        self.background_canvas = Canvas(self, width=self.x_y_values[0], height=self.x_y_values[1])

        ## Buttons - Main Frame
        self.tmd_button = Button(self, text='Model Conversion', command=self.convert_model, cursor='hand2')
        ## LabelFrame - Info and Conversion Result
        self.label_info = LabelFrame(self, text='Info... Ruff')
        self.label_dump = LabelFrame(self, text='Conversion Result')
        ## Label - Parent Info LabelFrame
        self.tmd_label = Label(self.label_info, text= f'Model Conversion: Convert a Model into DAE file format,\nif no animation data embedded or loaded,\nobjects will be placed at the retail Origin Point.', justify=CENTER)
        ## Text - Parent Conversion Result LabelFrame
        self.conversion_text = Text(self.label_dump)
        initial_text = f'||||---> TLoD TMD CONVERTER <---||||\nIMPORTANT NOTE: For TMD and CTMD Files from DEFF packages, \ntool will try to find embedded CMB/LMB/SAF animations'
        self.conversion_text.insert(INSERT, initial_text)
        self.conversion_text.config(state='disabled')
        ## ScrollBar for Text Dump
        self.scrollbar_text = Scrollbar(self.conversion_text, command=self.conversion_text.yview, cursor='arrow')
        ## About Button
        self.about_button = Button(self, text="About", command=self.execute_about, cursor='hand2')
        ## Github Hyperlink
        self.github_page = Label(self, text='https://github.com/Legend-of-Dragoon-Modding/TLoD-TMD-Converter', font=('Calibri', 11), fg='#0000EE', cursor='hand2')

        #### Placing Methods ####
        self.background_canvas.place(relwidth=1, relheight=1, relx=-0.28, rely= -0.25)
        self.background_canvas.create_image(self.x_y_values[0], self.x_y_values[1], image=self.image_background)
        self.tmd_button.place(relwidth=0.2, relheight=0.1, relx=0.40, rely=0.01)
        self.label_info.place(relx=0.26, rely=0.15, relwidth= 0.55, relheight= 0.23)
        self.label_dump.place(relx=0.26, rely=0.40, relwidth= 0.70, relheight= 0.53)
        self.tmd_label.place(relx=0.01, rely=0.01, relwidth= 0.9, relheight= 0.9)
        self.tmd_label.config(font=('Arial Black', 12), fg='#4578b0')
        self.conversion_text.place(relx=0.001, rely=0.01, relwidth= 0.99, relheight= 0.98)
        self.conversion_text.config(yscrollcommand=self.scrollbar_text.set)
        self.scrollbar_text.place(relx=0.975, rely=0, relwidth= 0.03, relheight= 1)
        self.about_button.place(relx=0.05, rely=0.75, relwidth= 0.15, relheight= 0.1)
        self.github_page.place(relx=0.05, rely=0.93, relwidth= 1, relheight= 0.07)
        self.github_page.bind("<Button-1>", lambda e: self.callback_link('https://github.com/Legend-of-Dragoon-Modding/TLoD-TMD-Converter'))
    
    def resize_window(self, width_mainframe_change=int, height_mainframe_change=int):
        self.image_width_changed = round((60 * width_mainframe_change) / 100)
        self.image_height_changed = round((60 * height_mainframe_change) / 100)
        self.tuple_xy_changed = self.image_width_changed, self.image_height_changed
        return self.tuple_xy_changed

    def execute_about(self): # About Button show
        message_about = f'TLoD TMD Converter BETA v0.1 \nCoded By DooMMetal (AKA DragoonSouls) 2023 ©\nThis Tool was made from fans to fans!, keep it as it is!\nVisit my Github for updates'
        self.message_box_win = messagebox.showinfo('About TLoD TMD Converter', message_about)
    
    def callback_link(self, url=str):
        webbrowser.open_new_tab(url)
    
    def convert_model(self):
        self.conversion_text.config(state='normal')
        model_to_convert = askopenfile(title=f'Select a Model file...')
        self.conversion_text.delete(1.0, END)
        if model_to_convert != None:
            model_path = model_to_convert.name
            try:
                tlod_tmd_converter.main(model_path)
                self.conversion_text.insert(INSERT, tlod_tmd_converter.fma.file_filter_text)
                if tlod_tmd_converter.fma.file_type == f'CTMD':
                    for each_prim_unpack in tlod_tmd_converter.md.ctd.primitive_conversion_info:
                        self.conversion_text.insert(INSERT, each_prim_unpack)
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.md.ctd.primitives_unpacked_info)
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.md.ctd.total_block_vertices_info)
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.md.ctd.vertices_converted_info)
                if tlod_tmd_converter.fma.animation_data_info[2] != f'NONE':
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.fma.animation_check_info)
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.afp.processing_anim)
                    if tlod_tmd_converter.afp.animation_type_check == f'SAF':
                        self.conversion_text.insert(INSERT, tlod_tmd_converter.afp.csaf.conversion_saf_ok)
                        self.conversion_text.insert(INSERT, tlod_tmd_converter.afp.csaf.finished_convert_saf)
                    elif tlod_tmd_converter.afp.animation_type_check == f'CMB':
                        self.conversion_text.insert(INSERT, tlod_tmd_converter.afp.ccmb.cmb_conversion_finished)
                    elif tlod_tmd_converter.afp.animation_type_check == f'LMB_Type_0':
                        self.conversion_text.insert(INSERT, tlod_tmd_converter.afp.clmb.lmb_conversion_finished)
                if tlod_tmd_converter.mf.check_this_mf_bool == True:
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.mf.retail_bugged_vertex_info)
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.mf.working_retail_bugged_info)
                for check_dup in tlod_tmd_converter.colcomp.check_duplicate_state:
                    self.conversion_text.insert(INSERT, check_dup)
                if tlod_tmd_converter.colcomp.check_bool == True:
                    self.conversion_text.insert(INSERT, tlod_tmd_converter.colcomp.winding_diff_info)
                self.conversion_text.insert(INSERT, tlod_tmd_converter.pr.total_number_vnp)
                self.conversion_text.insert(INSERT, tlod_tmd_converter.cw.collada_success)
            except OSError:
                error_text = f'\nNot a valid Model file...'
                self.conversion_text.insert(INSERT, error_text)
        else:
            error_text = f'\nYou must load a file...'
            self.conversion_text.insert(INSERT, error_text)
        self.conversion_text.config(state='disabled')


if __name__ == "__main__":
    main_window = Tk()
    main_window.iconbitmap(default='Resources/DD_Eye.ico')
    main_window.wm_title("TLoD TMD Converter BETA v0.1")
    width_native_windows = main_window.winfo_screenwidth()
    height_native_windows = main_window.winfo_screenheight()
    middle_place_width = (width_native_windows // 2) - (width_native_windows // 3)
    middle_place_height = (height_native_windows // 2) - (height_native_windows // 3)
    main_window.geometry(f'+{middle_place_width}+{middle_place_height}')

    ratio_width = round((55 * width_native_windows) / 100)
    ratio_height = round((55 * height_native_windows) / 100)

    tlod_tmd_converter_gui = TCWindow(main_window, width=ratio_width, height=ratio_height)
    tlod_tmd_converter_gui.mainloop()