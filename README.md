# KalmanVisualize
System for visualizing trajectory estimated by the Kalman filtering

The system contains plot_trajectory function which is used to draw trajectory from dataframe with three columns: 'x', 'y' and 'time', plot_uncertainty function which give additional modality - the uncertainty ellipse is added to each trajectory point. This ellipse is calculated using covariance matrices. Two exemplary estimations was attached - trajectory_test_1 (linear model) and trajectory_test_2 (non-linear model). Two more scripts: random and generate_cov_matrix is used to generate random data.

![image](https://github.com/TMarszalek129/KalmanVisualize/assets/168923361/6ef78554-e736-48a2-8505-745379cc9b72)
![image](https://github.com/TMarszalek129/KalmanVisualize/assets/168923361/a2cb3279-4c7b-4ae6-bcf3-3444f0a4b7c1)

![image](https://github.com/TMarszalek129/KalmanVisualize/assets/168923361/4a38aa41-0db0-48df-911f-0d72855be210)
![image](https://github.com/TMarszalek129/KalmanVisualize/assets/168923361/0cea9682-6501-4ec9-a0b9-cb537320f1c1)
![image](https://github.com/TMarszalek129/KalmanVisualize/assets/168923361/ecd17d11-dfac-49df-9efd-0a67157ca019)
![image](https://github.com/TMarszalek129/KalmanVisualize/assets/168923361/046d043a-44d8-4354-8eed-f07628aae58c)

Images sources:
- https://www.edrawsoft.com/article/bedroom-floor-plan-examples.html
- https://upload.wikimedia.org/wikipedia/commons/9/9a/Sample_Floorplan.jpg?fbclid=IwAR1Gkqb7y6T1DRlFuB_leaBZIJMgkAMoRFpOlP_BPTLkmHDz7x1QjlAjHbg
