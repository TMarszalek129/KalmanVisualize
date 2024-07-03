import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import matplotlib.colors
import pandas as pd

def plot_uncertainty(df : pd.DataFrame,
                    cov : np.ndarray,
                    plot : matplotlib.collections.PathCollection,
                    n : int = 1,
                    color_of_ellipse : str = 'red',
                    alpha_of_ellipse : float = 0.3,
                    save_path: str = None
                    ) -> matplotlib.collections.PathCollection:
    """
    Add ellipses showing uncertainty to plot with trajectory visualization

    Parameters
    ----------
    df : pd.DataFrame
        DESCRIPTION. Trajectory as  DataFrame with three columns: 'x', 'y' and 'time'
    cov : np.ndarray
        DESCRIPTION. Covariance matrices as three dimensions numpy array  (count of points, 2, 2)
    plot : matplotlib.collections.PathCollection
        DESCRIPTION. Figure with trajectory visualization returns by function plot_trajectory
    n : int
        DESCRIPTION. The default is 1 - number of standard deviation to use in scaling the ellipse
    color_of_ellipse : str, optional
        DESCRIPTION. The default is 'red' - color of ellipses, must comply with matplotlib standards: 
                                            https://matplotlib.org/stable/gallery/color/named_colors.html
    alpha_of_ellipse : float, optional
        DESCRIPTION. The default is 0.3 - alpha channel to define transparency of ellipses
    save_path : str, optional
        DESCRIPTION. The default is None - path to place where there will be plot saved

    Returns
    -------
    plot : matplotlib.collections.PathCollection
        DESCRIPTION. All graphical elements which this function shows

    """

    
    df = df.loc[:, ['x', 'y']]
    mean_x = df['x']
    mean_y = df['y']
    
    if alpha_of_ellipse < -1.0 or alpha_of_ellipse > 1.0:
        raise ValueError('Parameter \'alphaOfEllipse\' must be between 0.0 and 1.0')
    
    for i in range(len(cov)):
        pearson = cov[i,0,1]/np.sqrt(cov[i,0,0] * cov[i,1,1])
        if pearson < -1.0 or pearson > 1.0:
            raise ValueError('Pearson coefficient must be between -1.0 and 1.0')
        radius_x = np.sqrt(1 + pearson)
        radius_y = np.sqrt(1 - pearson)
        std_x = np.sqrt(cov[i,0,0]) * n
        std_y = np.sqrt(cov[i,1,1]) * n
        mx = mean_x[i]
        my = mean_y[i]
        
        ellipse = Ellipse((0,0), radius_x * 2, radius_y * 2, facecolor=color_of_ellipse, alpha=alpha_of_ellipse)
            
        transf = transforms.Affine2D().rotate_deg(45).scale(std_x, std_y).translate(mx, my)
            
        ellipse.set_transform(transf + plot.axes.transData)
        
        plot.axes.add_patch(ellipse)
        
        if save_path != None:
            plt.savefig(save_path, dpi=100)
    
    return plot


   
