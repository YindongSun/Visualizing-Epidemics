import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend


# Network topology
g = nx.erdos_renyi_graph(1000, 0.05)

# Model selection
model = ep.SISModel(g)

# Model Configuration
cfg = mc.Configuration()
cfg.add_model_parameter('beta', 0.01)
cfg.add_model_parameter('proability of return to S stage', 0.005)
cfg.add_model_parameter("initial infected rate", 0.05)
model.set_initial_status(cfg)

# Simulation execution
iterations = model.iteration_bunch(200)
trends = model.build_trends(iterations)

#visualize
viz = DiffusionTrend(model, trends)
p = viz.plot(width=550, height=550)
show(p)