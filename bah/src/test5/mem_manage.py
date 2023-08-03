import psutil
import os
import numpy as np
import plotly.graph_objects as go

MAX = 45000

ar = []
pr_mem = []
swap_mem = []
virt_mem = []

process = psutil.Process()

for i in range(MAX):
    ar.append(np.zeros(100_000))
    pr_mem.append(process.memory_info())
    swap_mem.append(psutil.swap_memory())
    virt_mem.append(psutil.virtual_memory())

# Extract the data for plotting
rss_data = [x.rss for x in pr_mem]
vms_data = [x.vms for x in pr_mem]
available_data = [x.available for x in virt_mem]
total_swap_data = [x.total for x in swap_mem]
used_swap_data = [x.used for x in swap_mem]
free_swap_data = [x.free for x in swap_mem]

# Create Plotly figure and add traces
fig = go.Figure()

fig.add_trace(go.Scatter(x=np.arange(MAX), y=rss_data, mode='lines', name='Resident Set Size'))
#fig.add_trace(go.Scatter(x=np.arange(MAX), y=vms_data, mode='lines', name='Virtual Memory Size'))
fig.add_trace(go.Scatter(x=np.arange(MAX), y=available_data, mode='lines', name='Available Memory'))
fig.add_trace(go.Scatter(x=np.arange(MAX), y=total_swap_data, mode='lines', name='Total Swap Memory'))
fig.add_trace(go.Scatter(x=np.arange(MAX), y=used_swap_data, mode='lines', name='Used Swap Memory'))
fig.add_trace(go.Scatter(x=np.arange(MAX), y=free_swap_data, mode='lines', name='Free Swap Memory'))

# Set the layout
fig.update_layout(title='Memory Statistics Over Time',
                  xaxis_title='Time',
                  yaxis_title='Memory (bytes)',
                  legend=dict(x=0.5, y=1.0, orientation='h'),
                  width=1000,
                  height=600)

# Show the plot
fig.show()