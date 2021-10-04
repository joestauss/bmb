from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict

def category_pairs( categories, reflexive=False):
    #   Returns a list of all category pairs.
    #   Single items are paired with themselves.
    #   Reflexive mode returns all permutations.
    pairs = list()
    if len( categories) == 1:
        category = categories[0]
        pairs.append(( category, category))
    else:
        for c, category in enumerate( categories):
            for i in range( c):
                pairs.append(( categories[i], category ))
                if reflexive:
                    pairs.append(( category, categories[i] ))
    return pairs


def cross_classification_heatmap( data, row_order=None, col_order=None, default_value=0):
    """ data should have the form ( row_category_1, col_category)
    """

    row_order = row_order if row_order else sorted(set((t[0] for t in data)))
    col_order = col_order if col_order else sorted(set((t[1] for t in data)))

    dd = defaultdict( lambda: defaultdict( lambda: 0))
    for x, y in data:
        dd[ y][ x] += 1

    heatmap_values = list()
    for col in col_order:
        heatmap_values.append( list())
        for row in row_order:
            if row in dd[ col]:
                heatmap_values[ -1].append( dd[ col][ row])
            else:
                heatmap_values[-1].append( default_value)

    plt.xticks(ticks=np.arange( len( row_order)), labels=row_order, rotation=80)
    plt.yticks(ticks=np.arange( len( col_order)), labels=col_order)
    plt.imshow( heatmap_values)
    plt.figure(figsize=(6, 6))
    plt.show()


def heatmap( data, row_order=None, col_order=None):
    def _all_categories( data):
        categories = set()
        for row in data.values():
            categories |= set( row.keys())
        return categories
    row_order = row_order if row_order else sorted( _all_categories( data))
    col_order = col_order if col_order else data.keys()

    heatmap_values = list()
    for col in col_order:
        heatmap_values.append( list())
        for row in row_order:
            if row in data[ col]:
                heatmap_values[ -1].append( data[ col][ row])
            else:
                heatmap_values[-1].append(0)

    plt.xticks(ticks=np.arange( len( row_order)), labels=row_order, rotation= 80)
    plt.yticks(ticks=np.arange( len( col_order)), labels=col_order)
    plt.imshow( heatmap_values)
