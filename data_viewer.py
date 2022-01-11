from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# DATAVIEWER


def dataviewer(dataframe):
    root = Tk()
    root.title('Data Viewer')

    app_width = 1000
    app_height = 600

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2.25) - (app_height / 2)

    root.geometry('{}x{}+{}+{}'.format(app_width, app_height, int(x), int(y)))
    root.iconbitmap('./satellite.ico')
    root.configure(background='#F8F9FA')

    columns = dataframe.columns
    rows = dataframe.to_numpy().tolist()

    dataviewer_frame = Frame(root, background='#F8F9FA')
    dataviewer_frame.grid(columnspan=2, sticky='nsew')

    horizontal_scroll = Scrollbar(dataviewer_frame, orient='horizontal')
    horizontal_scroll.grid(sticky='s')

    vertical_scroll = Scrollbar(dataviewer_frame)
    vertical_scroll.grid(sticky='e')

    dataviewer = ttk.Treeview(
        dataviewer_frame, xscrollcommand=horizontal_scroll.set, yscrollcommand=vertical_scroll.set, selectmode=NONE)

    horizontal_scroll.config(command=dataviewer.xview)
    vertical_scroll.config(command=dataviewer.yview)

    dataviewer['columns'] = list(columns)
    dataviewer['show'] = 'headings'

    for column in dataviewer['columns']:
        dataviewer.heading(column, text=column)

    for row in rows:
        dataviewer.insert('', 'end', values=row)

    list_of_children = dataviewer.get_children()

    # SAVING TO CSV

    def saving():
        file = filedialog.asksaveasfile(
            filetypes=[('CSV Files', '*.csv')], defaultextension='*.csv')
        dataframe.to_csv(file, index=False, line_terminator='\n')

        if file:
            messagebox.showinfo('Saving', 'Saved successfuly')

    count_label = Label(root, text='Displaying {} rows'.format(len(list_of_children)), bg='#F8F9FA')
    count_label.grid(row=1)

    save_as_csv_btn = Button(root, text='Save To Drive',
                             command=saving, bg='#DEE2E6')
    save_as_csv_btn.grid(row=1)

    dataviewer.grid(row=0, sticky='nsew')

    root.mainloop()
