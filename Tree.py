import fileinput
import math

'''
Node structure
array with possible values
final value of node

recursion, once used remove element from array
'''

def entropy(data_fields):

    #print('Function params'+str(data_fields))
    last_fields = [data[-1] for data in data_fields]

    #print("Last rows")
    #print(last_fields)

    uniques = []
    [uniques.append(unique) for unique in last_fields if unique not in uniques]

    #print("Values for entropy")
    #print(uniques)

    bot = len(last_fields)

    qty = [0] * len(uniques)
    for idx, unique in enumerate(uniques):
        for field in last_fields:
            if unique == field:
                qty[idx] += 1

    #print("Qyt")
    #print(qty)

    #print("Bot")
    #print(bot)

    counter = 0
    for idx in range(len(uniques)):
        counter += -(qty[idx]/bot)*(math.log(qty[idx]/bot, 2))

    #print("Entropy")
    #print(counter)
    return counter


def n_branch(uniques, elem, data):
    branches = [[] for idx in range(len(uniques))]
    for piece in data:
        for idx, unique in enumerate(uniques):
            if piece[elem] == unique:
                branches[idx].append(piece)
    #print('Branches' + str(branches))
    return branches


def get_uniques(data, element):
    uniques = []
    for unique in data:
        if unique[element] not in uniques:
            uniques.append(unique[element])
    return uniques


def get_gain(bot, system_entropy, branches, entropies):
    gain = system_entropy
    for enum, branch in enumerate(branches):
        gain -= (len(branch) / bot) * entropies[enum]
    return gain


def getKey(item):
    return item[-1][-1]


def d3node(data, system_entropy, depth, names):
    gains = []
    for element in range(len(data[0])-1):
        uniques = get_uniques(data, element)
        #print(uniques)
        branches = n_branch(uniques, element, data)
        entropies = [entropy(branch) for branch in branches]
        #print("Entropies"+str(entropies))
        gains.append(get_gain(len(data), system_entropy, branches, entropies))
    #print("gains"+str(gains))
    idxMax = gains.index(max(gains))
    uniques = get_uniques(data, idxMax)
    decide = n_branch(uniques, idxMax, data)
    #print(len(decide))
    #print(decide[0][-1])
    if decide[0][-1][-1] == 'FALSE':
        decide = reversed(decide)
    elif decide[0][-1][-2] == 'FALSE' and decide[0][-1][-1] != 'FALSE' and decide[0][-1][-1] != 'TRUE':
        decide = reversed(decide)
    for enum, option in enumerate(decide):
        print(' '*(depth)+str(names[idxMax][0])+': '+option[0][idxMax])#str(names[idxMax][1][enum-idxMax]))
        if entropy(option) == 0:
            print('  '*(depth+1)+'ANSWER: '+option[-1][-1])
        else:
            #del option[idxMax]
            d3node(option, system_entropy, depth+1, names)


if __name__ == '__main__':
    lines = []
    nodes = []
    names = []
    queries = []

    for line in fileinput.input():
        if line[0] != '%':
            line = line.strip('\n')
            line = line.replace(' ', '')
            line = line.replace('\t', '')
            if line != '':
                lines.append(line)

    #print(lines)

    name = ''
    for idx, line in enumerate(lines[1:]):
        values = []
        if line == "@data":
            break

        line = line[line.find('@attribute')+10:]
        name = line[:line.find('{')]
        values = line[line.find('{')+1:-1].split(',')
        #print(name)
        #print(values)
        names.append([name, values])
    data = []
    for line in lines[idx+2:]:
        data.append(line.split(','))

    #print("Data")
    #print(data)

    system_entropy = entropy(data)
    d3node(data, system_entropy, 0, names)
    #tree(data, system_entropy, 0)



    '''
    Calculate individual rows
    '''
    #print(data[2])

    '''
    while len(data) > 1:
        obtain_optimal(data)
    '''

