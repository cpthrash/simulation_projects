''' This script creates a table containing output data from multiple input files.  The output file is then fed into R for plotting of data from the multiple input files. 

The following is a reference list for choosing which column to pick from the MSstats output:


'''

import os
import glob
import csv
import re
import numpy

params = {
    'which_column':6
}

fileList = glob.glob('MSstats*') # Find all filenames that begin with 'MSstats'
print (fileList)

findPopSize = re.compile(r'MSstats_(\d+)') # Find the PopSize from the filename

popSizes = [] # Create an empty list that will store the various PopSizes from the simulations

for i in fileList: 
    size = findPopSize.search(i).groups()[0]
    popSizes.append(size) # Append the population size value from the filename to the list in "popSizes"

print(popSizes)


def createMultiTable(params):
    with open('testing.txt', 'a') as out:
        for i in popSizes: # For each item in the popSizes list
            # do stuff here
            out.write(i) # Write the item to the file 'testing.txt'
            out.write('\t') # # Write a tab to file 'testing.txt'
        out.write('\n') # Go to the next line of the 'testing.txt' file

        for i in fileList:
            with open(i, 'rb') as csvfile: # Open the file(s) in 'fileList'

                #get number of columns
                for line in csvfile.readlines(): # Read the lines in the list and return the lines as a list
                    array = line.split(' ')

                csvfile.seek(0) # Set the pointer to the beginning of the file 

                reader = csv.reader(csvfile, delimiter='\t') # Read the input file
                included_cols = params['which_column']  # Define which colum(s) will be extracted from the input file
                numpy.delete(csvfile, (0), axis=0)
                print csvfile

                with open('multiTable.txt', 'a') as outfile:
                    for row in reader:
                        content = list(row[i] for i in included_cols)
                        outfile.write('content' + '\t') # Print each item from 'content', which is only the included columns from each row, to the outfile

createMultiTable(params)

