from collections import defaultdict

def category_coincidence_count( category_combinations):
    """
    Returns a dict-of-dicts that contains the count of each pair.
    Single-value categories are counted along the diagonal.
    """
    pair_count = defaultdict( lambda: defaultdict( lambda: 0))
    categories = set()
    for category_combination in category_combinations:
        categories |= set(category_combination)

    for cat_1 in categories:
        for cat_2 in categories:
            pair_count[ cat_1][ cat_2]

    for category_combination in category_combinations:
        if len( category_combination) == 1:
            category = category_combination[0]
            pair_count[ category][ category] += 1

        else:
            for c, category in enumerate( category_combination):
                for i in range( c):
                    pair_count[ category_combination[i]][ category] += 1
                    pair_count[ category][ category_combination[i]] += 1
    return pair_count

def category_count( category_combinations):
    count = defaultdict( lambda: 0)
    for category_combination in category_combinations:
        for category in category_combination:
            count[ category] += 1
    return count
