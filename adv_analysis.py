import mongo
import data_utils


def advanced(norms, tokens, digest):
    freq_count = {}
    notFound = {}
    result = {}
    for element in tokens:
        freq_count[element] = tokens.count(element)
    for k, v in norms.items():
        for key in freq_count.keys():
            if k == key:
                value = v[:3]
                v = data_utils.cleanValues(value)
                result[key] = value
            if key not in norms.keys():
                notFound[key] = 'not found'
    return mongo.adv_insert(result, notFound,freq_count, digest)
