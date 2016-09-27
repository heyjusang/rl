import numpy

class Grid:

    @staticmethod
    def templeteGrid(templetePath)
        grid = []
        templeteFile = open(templetePath, 'r')
        for line in templeteFile.readlines():
            row = line.replace("\r", "").replace("\n", "").split("\t")
            grid.append(row)

        return grid
    
    @staticmethod
    def exprGrid(templeteGrid, genes, sampleIndex):
        grid = []
        for templeteRow in templeteGrid:
            row = []
            for name in templeteRow:
                if name in genes:
                    row.append(genes[name].getValue(sampleIndex))
                else:
                    row.append(0)
            grid.append(row)

        return numpy.array(grid)
