# KalmanVisualize
System for visualizing trajectory estimated by the Kalman filtering

The system contains plot_trajectory function which is used to draw trajectory from dataframe with three columns: 'x', 'y' and 'time', plot_uncertainty function which give additional modality - the uncertainty ellipse is added to each trajectory point. This ellipse is calculated using covariance matrices. Two exemplary estimations was attached - trajectory_test_1 (linear model) and trajectory_test_2 (non-linear model). Two more scripts: random and generate_cov_matrix is used to generate random data.
