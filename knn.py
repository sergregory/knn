#! /usr/bin/python
import numpy
from matplotlib import pyplot
import os
import heapq


def read_pgm(filename):
    """ read image from 8-bit PGM file
    """
    try:
        inFile = open(filename)

        header = None
        size = None
        maxGray = None
        data = []

        for line in inFile:
            stripped = line.strip()

            if stripped[0] == '#':
                continue
            elif header is None:
                if stripped != 'P2':
                    return None
                header = stripped
            elif size is None:
                size = map(int, stripped.split())
            elif maxGray is None:
                maxGray = int(stripped)
            else:
                for item in stripped.split():
                    data.append(int(item.strip()))

        data = numpy.reshape(data, (size[1], size[0]))
        return data

    except:
        pass

    return None


def euclidean_distance(a, b):
    a = numpy.reshape(a, (1, a.size))
    b = numpy.reshape(b, (1, b.size))
    c = a - b
    return numpy.vdot(c, c)


def find_nearest(obj, objects):
    min_index, min_value = min(enumerate(objects), key=(lambda x: euclidean_distance(obj, x[1])))
    return min_index

def find_k_nearest(k, obj, objects):
    nearest = heapq.nsmallest(k, enumerate(objects), key=(lambda x: euclidean_distance(obj, x[1])))
    ind = [o[0] for o in nearest]
    return ind

def majority_vote(variants):
    '''
    '''
    count = {}
    for v in variants:
        if v in count:
            count[v] += 1
        else:
            count[v] = 1
    vote = max(count.items(), (lambda x: x[1]))
    return vote[0][0]

def load_data(path):
    files = os.listdir(train_data_dir)
    files = filter((lambda name: name.endswith(".pgm")), files)
    # print files
    files = map((lambda name: os.path.join(train_data_dir, name)), files)
    data = map(read_pgm, files)
    # data = map((lambda d: numpy.reshape(d, (1, d.size))), data)
    return data


if __name__ == "__main__":
    train_data_dir = os.path.join(os.getcwd(), "data/train")
    test_data_dir =  os.path.join(os.getcwd(), "data/test")

    train_data = load_data(train_data_dir)
    test_data = load_data(test_data_dir)

    labels = numpy.fromfile(os.path.join(train_data_dir, "labels.txt"), dtype=int, sep='\n')

    for img in test_data:
        # pyplot.imshow(img, pyplot.cm.gray)
        # pyplot.show()
        ind = find_nearest(img, train_data)
        nearest_labels = [labels[neighbour] for neighbour in find_k_nearest(5, img, train_data)]
        vote = majority_vote(nearest_labels)
        print (labels[ind], vote)
