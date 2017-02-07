import mongo
import data_utils


def advanced( option, norms, tokens, digest):
    # tokens = []
    freq_count = {}
    notFound = {}
    result = {}
    values = {}
    value = []
    rank = {}
    associationvalue = 0
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
    for k1, v1 in freq_count.items():
        for k2, v2 in result.items():
            occfreq = freq_count[k2]
            item = result[k2][int(option)]
            for k, v in item.items():
                associationvalue = v
            rank[k2] = int(associationvalue) * int(occfreq)
    tupleList = [(k, v) for k, v in rank.items()]
    sortedRank = sorted(tupleList, key=lambda x:x[1],reverse=True)
    return mongo.adv_insert(result, notFound,freq_count, digest, sortedRank)
