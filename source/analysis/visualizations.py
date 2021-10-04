from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict
from matplotlib  import pyplot as plt
from collections import defaultdict
from bmb.source.cross_classification import heatmap
import math
import seaborn as sns

def _dictionary_to_2d_array( data, col_order, row_order):
    # data has format dd[col][row] = value
    return [[ data[ col][ row]
        for row in row_order ]
        for col in col_order ]

def visualize_categorical_association(
    data,
    total_count,
    category_1_count,
    category_2_count,
    category_1_order,
    category_2_order,
    title="Count of Input Data",
    figsize=(6, 6)):

    figsize = (0.75 * len(category_2_order), 0.5 * len(category_1_order))

    actual = defaultdict( lambda: defaultdict( lambda: 0))
    for cat1, cat2 in data:
        actual[ cat1][ cat2]    += 1


    expected = { a: {b:
                     category_1_count[a] * category_2_count[b] / total_count
                for b in category_2_order} for a in category_1_order}

    absolute_error = { a: {b:
                     actual[a][b] - expected[a][b]
                for b in category_2_order} for a in category_1_order}

    relative_error = { a: {b:
                 absolute_error[a][b] / expected[a][b]
                for b in category_2_order} for a in category_1_order}

    plt.figure(figsize=figsize)
    plt.title( title)
    sns.heatmap(
        _dictionary_to_2d_array( actual, category_1_order, category_2_order),
        cmap="Blues",
        yticklabels = category_1_order,
        xticklabels = category_2_order,
        annot=True,
        fmt="d"
    )

    plt.figure(figsize=figsize)
    plt.title( "Count Expected for Unassociated Categories")
    sns.heatmap(
        _dictionary_to_2d_array( expected, category_1_order, category_2_order),
        cmap="Blues",
        yticklabels = category_1_order,
        xticklabels = category_2_order,
        annot=True,
        fmt=".0f"
    )

    plt.figure(figsize=figsize)
    plt.title( "Strength of Association")
    sns.heatmap(
        _dictionary_to_2d_array( relative_error, category_1_order, category_2_order),
        cmap="RdYlGn",
        yticklabels = category_1_order,
        xticklabels = category_2_order,
        annot=True,
        fmt=".0%",
        center=0,
        vmin=-1,
        vmax=1
    )

def _all_categories( data):
    categories = set()
    for row in data.values():
        categories |= set( row.keys())
    return categories


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
    plt.show()

def categorical_heatmap( data, order=None, row_order=None, col_order=None):
    row_order = row_order if row_order else order if order else sorted( _all_categories( data))
    col_order = col_order if col_order else order if order else data.keys()

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
    plt.show()
