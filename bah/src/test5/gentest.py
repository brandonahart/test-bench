import rpy2.robjects as robjects
import gc
import time
import psutil

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


#import the R script
robjects.r('source("gentest.R")')

def run_genmat(n, size):
    start_time = time.time()
    start_mem = psutil.Process().memory_info().rss

    robjects.r('aframe <- genmat({}, {})'.format(n, size))

    elapsed_time = time.time() - start_time
    memory_consumed = (psutil.Process().memory_info().rss - start_mem)

    size = robjects.r("obj_size(aframe)")
    print(f"aframe size in R: {size}")
    robjects.r('aframe <- NULL')
    robjects.r('gc()')

    gc.collect()
    return elapsed_time, memory_consumed


def run_gendf(n, size):
    start_time = time.time()
    start_mem = psutil.Process().memory_info().rss
    start_fault = psutil.Process().memory_full_info().pfaults

    robjects.r('aframe <- gendf({}, {})'.format(n, size))

    elapsed_time = time.time() - start_time
    memory_consumed = (psutil.Process().memory_info().rss - start_mem)
    total_faults = (psutil.Process().memory_full_info().pfaults - start_fault)

    size = robjects.r("obj_size(aframe)")
    print(f"aframe size in R: {size}")
    robjects.r('aframe <- NULL')
    robjects.r('gc()')

    gc.collect()
    return elapsed_time, memory_consumed, total_faults


# Parameters
n = 1000000
size = 10

x1_arr = []
x2_arr = []
y1_arr = []
y2_arr = []

# Run genmat() and time it
for i in range(1,20):
    x1_arr.append(i)
    print(f"Number of rows: {n*i}")
    elapsed_time, memory_consumed = run_genmat(n*i, size)
    y1_arr.append(memory_consumed)
    print(f"Elapsed Time: {elapsed_time:.4f} seconds")
    print(f"Memory Consumed: {memory_consumed}\n")


# Run gendf() and time it
for i in range(1,20):
    x2_arr.append(i)
    print(f"Number of rows: {n*i}")
    elapsed_time, memory_consumed, total_faults = run_gendf(n*i, size)
    y2_arr.append(memory_consumed)
    print(f"Elapsed Time: {elapsed_time:.4f} seconds")
    print(f"Memory Consumed: {memory_consumed}\n")


# use specs parameter in make_subplots function
# to create secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])
 
# plot a scatter chart by specifying the x and y values
# Use add_trace function to specify secondary_y axes.
fig.add_trace(
    go.Scatter(x=x2_arr, y=y1_arr, name="yaxis1 genmat values"),
    secondary_y=False)
 
# Use add_trace function and specify secondary_y axes = True.
fig.add_trace(
    go.Scatter(x=x2_arr, y=y2_arr, name="yaxis2 gendf values"),
    secondary_y=True,)

# Naming y-axes
fig.update_yaxes(title_text="<b>genmat</b> Y - axis ", secondary_y=False)
fig.update_yaxes(title_text="<b>gendf</b> Y - axis ", secondary_y=True)
fig.show()