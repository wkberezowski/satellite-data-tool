from tkinter import *
from tkinter import font
from tkinter.ttk import Treeview
from tkinter import messagebox
from tkinter import filedialog
from turtle import width
import matplotlib.pyplot as plt
import pylab
import scipy.stats as stats

# DATAVIEWER


def dataviewer(dataframe):
    root = Tk()
    root.title('Data Viewer')

    app_width = 1500
    app_height = 750

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

    dataviewer_h_scroll = Scrollbar(dataviewer_frame, orient='horizontal')
    dataviewer_h_scroll.pack(side=BOTTOM, fill=X)

    dataviewer_v_scroll = Scrollbar(dataviewer_frame)
    dataviewer_v_scroll.pack(side=RIGHT, fill=Y)

    dataviewer = Treeview(
        dataviewer_frame, xscrollcommand=dataviewer_h_scroll.set, yscrollcommand=dataviewer_v_scroll.set, selectmode=NONE)

    dataviewer_h_scroll.config(command=dataviewer.xview)
    dataviewer_v_scroll.config(command=dataviewer.yview)

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

    try:

        statistics = [
            ['MIN', *list(dataframe.min().astype(float).round(3))],
            ['MAX', *list(dataframe.max().astype(float).round(3))],
            ['MEAN', *list(dataframe.mean().astype(float).round(3))],
            ['STANDARD DEVIATION', *
                list(dataframe.std().astype(float).round(3))],
            ['VARIANCE', *
                list(dataframe.var().astype(float).round(3))],
            ['SKEWNESS', *
                list(dataframe.skew().astype(float).round(3))],
            ['KURTOSIS', *
                list(dataframe.kurtosis().astype(float).round(3))],
        ]

        statistics_frame = Frame(root)
        statistics_frame.pack(side=LEFT, padx=10)

        statistics_h_scroll = Scrollbar(statistics_frame, orient='horizontal')
        statistics_h_scroll.pack(side=BOTTOM, fill=X)

        statistics_v_scroll = Scrollbar(statistics_frame, orient='vertical')
        statistics_v_scroll.pack(side=RIGHT, fill=Y)

        statistics_table = Treeview(statistics_frame, xscrollcommand=statistics_h_scroll.set,
                                    yscrollcommand=statistics_v_scroll.set, selectmode=NONE)

        statistics_h_scroll.config(command=statistics_table.xview)
        statistics_v_scroll.config(command=statistics_table.yview)

        statistics_table['columns'] = ['statistic', *list(columns)]
        statistics_table['show'] = 'headings'

        for column in statistics_table['columns']:
            statistics_table.heading(column, text=column, width=10)

        for row in statistics:
            statistics_table.insert('', 'end', values=row)

        statistics_table.pack()

    except ValueError:
        Label(root, text="COLUMN WITH STRING VALUES DETECTED! CANNOT SHOW STATISTICS!",
              bg='#F8F9FA', font=('Helvetica 14 bold')).pack(side=LEFT, padx=20)

    def plot_2D():
        plt.close('all')
        list_of_columns = []
        for column in dataframe.columns:
            list_of_columns.append(dataframe[column])
        if len(list_of_columns) != 2:
            messagebox.showerror(
                title="ERROR", message="For 2D plots you must select 2 columns")
        else:
            dataframe.plot()
            plt.show()

    def plot_3D():
        plt.close('all')
        list_of_columns = []
        for column in dataframe.columns:
            list_of_columns.append(dataframe[column])

        if len(list_of_columns) < 3:
            messagebox.showerror(
                title='ERROR', message='For 3D plots you must select 3 columns')
        else:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter3D(*list_of_columns)
            plt.show()

    def plot_hist():
        plt.close('all')
        dataframe.plot.hist()
        plt.show()

    def plot_q_q():
        plt.close('all')
        list_of_columns = []
        for column in dataframe.columns:
            list_of_columns.append(list(dataframe[column]))
        if len(list_of_columns) > 1:
            messagebox.showerror(
                title='ERROR', message='For the Q-Q plot you must select only one column')
        else:
            stats.probplot(*list_of_columns, plot=pylab)
            pylab.show()

    def plot_scatter():
        plt.close('all')
        list_of_columns = list(dataframe.columns)
        dataframe.plot.scatter(list_of_columns[0], list_of_columns[1])
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
    btn_2d_plot.grid(row=0, column=0, padx=10, pady=5)

    btn_3d_plot = Button(
        plots_frame, image=list_of_images[1], text='3D-Plot', compound=TOP, bg='#DEE2E6', command=plot_3D)
    btn_3d_plot.grid(row=0, column=1, padx=10, pady=5)

    btn_histogram = Button(
        plots_frame, image=list_of_images[2], text='Histogram', compound=TOP, bg='#DEE2E6', command=plot_hist)
    btn_histogram.grid(row=0, column=2, padx=10, pady=5)

    btn_qq_plot = Button(
        plots_frame, image=list_of_images[3], text='Q-Q-Plot', compound=TOP, bg='#DEE2E6', command=plot_q_q)
    btn_qq_plot.grid(row=0, column=3, padx=10, pady=5)

    btn_scatter_plot = Button(
        plots_frame, image=list_of_images[4], text='Scatter-Plot', compound=TOP, bg='#DEE2E6', command=plot_scatter)
    btn_scatter_plot.grid(row=0, column=4, padx=10, pady=5)

    root.mainloop()
