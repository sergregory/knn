import numpy
from matplotlib import pyplot


def read_pgm(filename):

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

if __name__ == "__main__":
    image = read_pgm("data/test/image_00000.pgm")
    pyplot.imshow(image, pyplot.cm.gray)
    pyplot.show()
