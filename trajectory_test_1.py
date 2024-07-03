import numpy as np
import pandas as pd
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
from filterpy.common import Saver
from plot_trajectory import plot_trajectory
from plot_uncertainty import plot_uncertainty


def create_measurements(var_Q, var_R, count, dt=1):
    
    np.random.seed(121)
    std_Q = np.sqrt(var_Q)
    std_R = np.sqrt(var_R)
    
    x, y = 0, 0
    vel_x, vel_y = 5, 2.5
    
    t = 0
    
    zx, zy = [], []
    time = []
    
    for _ in range(count):
        v_x = vel_x + np.random.randn() * std_Q 
        v_y = vel_y + np.random.randn() * std_Q
        x = x + v_x * dt 
        y = y + v_y * dt
        
        zx.append(x + (np.random.randn() * std_R))
        zy.append(y + (np.random.randn() * std_R))
        time.append(t)
        t += dt
    
    return zx, zy, time

def plot_model(plot, count):
    x = np.linspace(0, 15, count)
    y = 1/2 * x
    
    plot.axes.plot(x, y, 'b-')
    

def kalman_model(x, var_P, var_R, var_Q, dt=1):
    
    
    kf = KalmanFilter(dim_x=4, dim_z=2)
    kf.x = np.array([x[0], x[1], x[2], x[3]])
    kf.F = np.array([[1, dt, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, dt],
                     [0, 0, 0, 1]])
    kf.H = np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0]])
    kf.R  = np.array([[var_R, 0],
                     [0, var_R]])
    kf.P *= var_P
    q = Q_discrete_white_noise(dim=2, dt=dt, var=var_Q)
    kf.Q[0,0] = q[0,0]
    kf.Q[1,1] = q[0,0]
    kf.Q[2,2] = q[1,1]
    kf.Q[3,3] = q[1,1]
    kf.Q[0,2] = q[0,1]
    kf.Q[2,0] = q[0,1]
    kf.Q[1,3] = q[0,1]
    kf.Q[3,1] = q[0,1]
    return kf

def run_model(x0, var_P, var_Q, var_R, count, dt):
    
    zx, zy, t = create_measurements(var_Q, var_R, count, dt)
    
    kf = kalman_model(x0, var_P, var_R, var_Q, dt)
    
    x, cov = [], []
    saver = Saver(kf)
    for z_x, z_y in zip(zx, zy):
        #print(kf.Q)
        kf.predict()
        kf.update(np.array([z_x, z_y]))
        saver.save()
        #print(kf.x)
        x.append(kf.x)
        cov.append(kf.P)
        #print(kf.P)
        
    x, cov = np.array(x), np.array(cov)
    
    
    d = {'x' : x[:,0], 'y' : x[:,2], 'time' : t}
    df = pd.DataFrame(d)
    df['time'] = round(df.get('time'), 2)
    cov2drawU = []
    for c in cov:
        covi = [[
            c[0,0], c[0,2]],
             [c[2,0], c[2,2]]]
        cov2drawU.append(covi)
    
    cov2drawU = np.array(cov2drawU)
    cov = cov2drawU
    
    #plt.plot(x[0], x[1], zx, zy)
    plot = plot_trajectory(df)
    plot = plot_uncertainty(df, cov, plot, alpha_of_ellipse=0.2, n=3)
    plot = plot_trajectory(df)
    plot = plot_uncertainty(df, cov, plot, alpha_of_ellipse=0.1, n=3)
    plot_model(plot, count)
    #plt.xlim([0., 10.])
    #plt.ylim([0., 10.])
    
    return x, cov, df, saver, plot

dt = .1
x, cov, df, save, plot = run_model(x0 = [0, 0, 0, 0], var_P= 500, var_Q=1.0, var_R=1.5, count=30, dt=dt)