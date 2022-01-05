from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


def dataviewer(dataframe):
    root = Tk()
    root.title('Data Viewer')
    root.geometry('800x600')
    root.iconbitmap('./satellite.ico')
    root.configure(background='#F8F9FA')

    columns = dataframe.columns
    rows = dataframe.to_numpy().tolist()

    dataviewer_frame = Frame(root, background='#F8F9FA')
    dataviewer_frame.pack(pady=20)

    horizontal_scroll = Scrollbar(dataviewer_frame, orient='horizontal')
    horizontal_scroll.pack(side=BOTTOM, fill=X)

    vertical_scroll = Scrollbar(dataviewer_frame)
    vertical_scroll.pack(side=RIGHT, fill=Y)

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

    def saving():
        file = filedialog.asksaveasfile(
            filetypes=[('CSV Files', '*.csv')], defaultextension='*.csv')
        dataframe.to_csv(file, index=False)

        if file:
            messagebox.showinfo('Saving', 'Saved successfuly')

    save_as_csv_btn = Button(root, text='Save To Drive',
                             command=saving, bg='#DEE2E6')
    save_as_csv_btn.pack(anchor=CENTER)

    dataviewer.pack()

    root.mainloop()
