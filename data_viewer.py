from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
# import warnings
# warnings.filterwarnings("ignore")

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
    root.iconbitmap('./images/satellite.ico')
    root.configure(background='#F8F9FA')

    columns = dataframe.columns
    rows = dataframe.to_numpy().tolist()

    dataviewer_frame = Frame(root, background='#F8F9FA')
    dataviewer_frame.pack(pady=10)

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

    list_of_children = dataviewer.get_children()

    # SAVING TO CSV

    def saving():
        file = filedialog.asksaveasfile(
            filetypes=[('CSV Files', '*.csv')], defaultextension='*.csv')
        dataframe.to_csv(file, index=False, line_terminator='\n')

        if file:
            messagebox.showinfo('Saving', 'Saved successfuly')

    count_label = Label(root, text='Displaying {} rows'.format(
        len(list_of_children)), bg='#F8F9FA')
    count_label.pack(pady=5)

    save_as_csv_btn = Button(root, text='Save To Drive',
                             command=saving, bg='#DEE2E6')
    save_as_csv_btn.pack(pady=5)

    dataviewer.pack()

    statistics = [
        ['MIN', *list(dataframe.min())],
        ['MAX', *list(dataframe.max())],
        ['MEAN', *list(dataframe.mean())],
        ['STANDARD DEVIATION', *list(dataframe.std())],
        ['VARIANCE', *list(dataframe.var())],
        ['SKEWNESS', *list(dataframe.skew())],
        ['KURTOSIS', *list(dataframe.kurtosis())],
    ]
    statistics_frame = Frame(root)
    statistics_frame.pack()

    statistics_table = ttk.Treeview(statistics_frame)
    statistics_table['columns'] = ['statistic', *list(columns)]
    statistics_table['show'] = 'headings'

    for column in statistics_table['columns']:
        statistics_table.heading(column, text=column)

    for row in statistics:
        statistics_table.insert('', 'end', values=row)

    statistics_table.pack()

    # if FutureWarning:
    #     messagebox.showwarning(
    #         title='ERROR', message='One of the variables in the file is in text format. Cannot show the statistics for that variable properly!')

    root.mainloop()
