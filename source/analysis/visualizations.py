from matplotlib import pyplot as plt
import numpy as np

def categorical_heatmap( data, order=None, plot=plt):
    order = order if order else data.keys()

    heatmap_values = list()
    for outer_category in order:
        heatmap_values.append( list())
        for inner_category in order:
            if inner_category in data[ outer_category]:
                heatmap_values[ -1].append( data[ outer_category][ inner_category])
            else:
                heatmap_values[-1].append(0)

    plot.xticks(ticks=np.arange( len( order)), labels=order, rotation= 80)
    plot.yticks(ticks=np.arange( len( order)), labels=order)

    plot.imshow( heatmap_values)
