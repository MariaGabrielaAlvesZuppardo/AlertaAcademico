def merge(left, right, key=lambda x: x):
    """Função auxiliar para mesclar duas listas ordenadas."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(lst, key=lambda x: x):
    """Implementação do Merge Sort."""
    if len(lst) <= 1:
        return lst

    mid = len(lst) // 2
    left = merge_sort(lst[:mid], key)
    right = merge_sort(lst[mid:], key)

    return merge(left, right, key)
