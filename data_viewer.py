from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt

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

    dataviewer = Treeview(
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
    statistics_frame.pack(side=LEFT, padx=10)

    statistics_table = Treeview(statistics_frame, selectmode=NONE)

    statistics_table['columns'] = ['statistic', *list(columns)]
    statistics_table['show'] = 'headings'

    for column in statistics_table['columns']:
        statistics_table.heading(column, text=column)

    for row in statistics:
        statistics_table.insert('', 'end', values=row)

    statistics_table.pack()

    def plot_2D():
        dataframe.plot()
        plt.show()

    plots_frame = Frame(root, bg='#F8F9FA')
    plots_frame.pack(side=RIGHT, padx=50)

    # IMAGES

    list_of_images = [PhotoImage(master=root, file='./images/2-d-plot.png'),
                      PhotoImage(master=root, file='./images/3-d-plot.png'),
                      PhotoImage(master=root, file='./images/histogram.png'),
                      PhotoImage(master=root, file='./images/q-q-plot.png'),
                      PhotoImage(master=root, file='./images/scatter-plot.png')]

    # BUTTONS FOR PLOTS

    btn_2d_plot = Button(
        plots_frame, image=list_of_images[0], text='2D-Plot',  compound=TOP, bg='#DEE2E6', command=plot_2D)
    btn_2d_plot.grid(row=0, column=0, padx=5, pady=5)

    btn_3d_plot = Button(
        plots_frame, image=list_of_images[1], text='3D-Plot', compound=TOP, bg='#DEE2E6')
    btn_3d_plot.grid(row=0, column=1, padx=5, pady=5)

    btn_histogram = Button(
        plots_frame, image=list_of_images[2], text='Histogram', compound=TOP, bg='#DEE2E6')
    btn_histogram.grid(row=1, column=0, padx=5, pady=5)

    btn_qq_plot = Button(
        plots_frame, image=list_of_images[3], text='Q-Q-Plot', compound=TOP, bg='#DEE2E6')
    btn_qq_plot.grid(row=1, column=1, padx=5, pady=5)

    btn_scatter_plot = Button(
        plots_frame, image=list_of_images[4], text='Scatter-Plot', compound=TOP, bg='#DEE2E6')
    btn_scatter_plot.grid(row=2, column=0, padx=5, pady=5)

    root.mainloop()
