import rpy2.robjects as robjects
import gc
import time
import psutil

import plotly.express as px


#import the R script
robjects.r('source("gentest.R")')

def run_gendf(n, size):
    start_time = time.time()
    robjects.r('aframe <- gendf({}, {})'.format(n, size))
    elapsed_time = time.time() - start_time

    robjects.r('aframe <- NULL')
    robjects.r('gc()')

    gc.collect()
    return elapsed_time


# Parameters
n = 1000000
size = 10

x_arr = []
y_arr = []
# Run gendf() and time it
for i in range(1,20):
    memory_usage = psutil.Process().memory_info().rss

    x_arr.append(i)
    print(f"Number of columns: {n*i}")

    elapsed_time = run_gendf(n*i, size)
    y_arr.append(elapsed_time)
    print(f"Elapsed Time: {elapsed_time:.4f} seconds")

    memory_consumed = (psutil.Process().memory_info().rss - memory_usage) / (1024 * 1024)
    print(f"Memory Consumed: {memory_consumed}\n")



fig = px.scatter(x=x_arr, y=y_arr)
fig.show()