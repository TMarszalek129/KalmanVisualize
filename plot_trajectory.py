import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import traja

def plot_trajectory(df : pd.DataFrame,
                   background : str = None,
                   s : float = 20.,
                   x_label: str = None,
                   y_label: str = None,
                   xy_unit: str = 'm',
                   time_unit : str = 's',
                   title: str = None,
                   x_lim: list = None,
                   y_lim: list = None,
                   show_grid: bool = False,
                   show_path : bool = True,
                   alpha_path: float = 0.3,
                   save_path: str = None
                   ) -> matplotlib.collections.PathCollection:
    """
    Plot trajectory for one object

    Parameters
    ----------
    df : pd.DataFrame
        DESCRIPTION. Trajectory as  DataFrame with three columns: 'x', 'y' and 'time'
    background : str, optional
        DESCRIPTION. The default is None - path to image which should be located in background,
                                            if parameter is None, there will not be image in background
    x_label : str, optional
        DESCRIPTION. The default is None - label to x-axis,
                                            if parameter is None, label will be 'position x [%xy_unit] -
                                            show below
    y_label : str, optional
        DESCRIPTION. The default is None - label to y-axis,
                                            if parameter is None, label will be 'position y [%xy_unit] -
                                            show below
    xy_unit : str, optional
        DESCRIPTION. The default is 'm' - position unit
    show_grid : bool, optional
        DESCRIPTION. The default is False - if True there will be grid in plot
    show_path : bool, optional
        DESCRIPTION. The default is True - if True there will be path connecting points in plot
    alpha_path : float, optional
        DESCRIPTION. The default is 0.3 - alpha channel to define transparency of path
    save_path : str, optional
        DESCRIPTION. The default is None - path to place where there will be plot saved
    s : float, optional
        DESCRIPTION. The default is 20.0 - size of dots which shows position in subsequent estimates
    time_unit : str, optional
        DESCRIPTION. The default is 's' - time unit
    title : str, optional
        DESCRIPTION. The default is None - title of plot,
                                            if parameter is None, title will not be
    x_lim : list, optional
        DESCRIPTION. The default is None - limitations of x-axis,
                                            if parameter is None, limitations will be calculate as
                                            min(x) - 1, min(x) + 1,
                                            limitation must be imputed as two-elements list
    y_lim : list, optional
        DESCRIPTION. The default is None - limitations of y-axis,
                                            if parameter is None, limitations will be calculate as
                                            min(y) - 1, min(y) + 1,
                                            limitation must be imputed as two-elements list

    Returns
    -------
    plot : matplotlib.collections.PathCollection
        DESCRIPTION. All graphical elements which this function shows

    """
    df = traja.TrajaDataFrame(df)
    
    if x_label == None:
        x_label = 'position x'
    if y_label == None:
        y_label = 'position y'
   
    x_label = x_label +  '[{:s}]'.format(xy_unit)
    y_label = y_label +  '[{:s}]'.format(xy_unit)
   
    if x_lim == None:
        x_lim = [min(df['x']) - 1, max(df['x']) + 1]
    
    if y_lim == None:
        y_lim = [min(df['y']) - 1, max(df['y']) + 1]
    
    plot = traja.plotting.plot(df, time_units = time_unit, title = title, s = s, xlim = x_lim, ylim = y_lim)
    
    if show_grid:
        plot.axes.grid()
    
    if background != None:
        im_back = plt.imread(background)
        plot.axes.imshow(im_back, extent=[x_lim[0], x_lim[1], y_lim[0], y_lim[1]])
    
    plot.axes.set_xlabel(x_label)
    plot.axes.set_ylabel(y_label)
   
    if show_path == False:
        plot.axes.patches[0].set_edgecolor('none')
    
    if  0.0 <= alpha_path <= 1.0:
        plot.axes.patches[0].set_alpha(alpha_path)
    else:
        raise ValueError('Parameter \'alpha_path\' must be between 0.0 and 1.0')
    
    if save_path != None:
        plt.savefig(save_path, dpi=100)
   
    return plot
    



