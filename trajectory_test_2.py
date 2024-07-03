import numpy as np
import pandas as pd
from filterpy.kalman import UnscentedKalmanFilter
from filterpy.kalman import MerweScaledSigmaPoints
from filterpy.common import Q_discrete_white_noise
from plot_trajectory import plot_trajectory
from plot_uncertainty import plot_uncertainty


def create_measurements(var_Q, var_R, count, dt=1):
    
    np.random.seed(156)
    std_Q = np.sqrt(var_Q)
    std_R = np.sqrt(var_R)
    
    x, y = 0, 0
    vel_x, vel_y = 5, 2.5
    acc_x, acc_y = 0, 2
    t = 0
    
    zx, zy = [], []
    time = []
    
    for _ in range(count):
        acc_x = 0 + np.random.randn() * std_Q
        acc_y = 2 + np.random.randn() * std_Q
        vel_x = 5 + dt * acc_x  
        vel_y = vel_y + dt * acc_y
        if(x >= 10 and y <= 10):
            x = x
            y = y + vel_y * dt
        elif(y >= 10 and x <= 10):
            x = x + vel_x * dt 
            y = y
        elif(x >= 10 and y >= 10):
            x = x
            y = y
        else:
            x = x + vel_x * dt 
            y = y + vel_y * dt
        
        zx.append(x + (np.random.randn() * std_R))
        zy.append(y + (np.random.randn() * std_R))
        time.append(t)
        t += dt
    
    return zx, zy, time

def hx(x):
    H = np.array([[1, 0, 0, 0],
                  [0, 0, 1, 0]])
    return H @ x
def fx(x, dt):
    if(x[0] >= 10 and x[2] <= 10):
        F = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, dt],
                      [0, 0, 0, 1]])
        B = np.array([[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 1]])
        u = np.array([0, 0, 0, 2])
    elif(x[2] >= 10 and x[0] <= 10):
        F = np.array([[1, dt, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])
        B = np.array([[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 1]])
        u = np.array([0, 0, 0, 2])
    elif(x[0] >= 10 and x[2] >= 10):
        F = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])
        B = np.array([[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 1]])
        u = np.array([0, 0, 0, 2])
    else:
        F = np.array([[1, dt, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, dt],
                      [0, 0, 0, 1]])
        B = np.array([[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 1]])
        u = np.array([0, 0, 0, 2])

    x = np.dot(F,x) + np.dot(B,u)
    
    return x

def plot_model(plot, count):
    x = np.linspace(0, 60, count)
    y = 0.5 * x + 0.055 * x**2
    
    plot.axes.plot(x, y, 'b-')
    

def kalman_model(x, var_P, var_R, var_Q, dt=1):
    
    sigmas = MerweScaledSigmaPoints(n=4, alpha=.3, beta=2., kappa=.1)
    kf = UnscentedKalmanFilter(dim_x=4, dim_z=2, dt=dt, hx=hx, fx=fx, points=sigmas)
    kf.x = np.array([x[0], x[1], x[2], x[3]])
    
    kf.R  = np.array([[var_R, 0],
                     [0, var_R]])
    kf.P *= var_P
    #print(kf.P)
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
    #saver = Saver(kf)
    for z_x, z_y in zip(zx, zy):
        
        kf.predict()
        kf.update(np.array([z_x, z_y]))
        #saver.save()
        
        x.append(kf.x)
        cov.append(kf.P)
        
    
    x, cov = np.array(x), np.array(cov)
    
   # print(x)
    d = {'x' : x[:,0], 'y' : x[:,2], 'time' : t}
    
    df = pd.DataFrame(d)
    df['time'] = round(df.get('time'))
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
    plot = plot_uncertainty(df, cov, plot, alpha_of_ellipse=0.1, n=3)
    plot = plot_trajectory(df)
    plot = plot_uncertainty(df, cov, plot, alpha_of_ellipse=0.1, n=3)
    plot_model(plot, count)
    
    
    return x, cov, df, plot

dt = .1
x, cov, df, plot = run_model(x0 = [0, 0, 0, 0], var_P= 500, var_Q=1.5, var_R=1.5, count=60, dt=dt)