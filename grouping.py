#!/usr/bin/python

import sys
import random
import xlrd

class run_grouping(object):
    def __init__(self, namefile, conflicts_file, num_of_groups):
        self.namefile = namefile
        self.conflicts_file = conflicts_file
        self.num_of_groups = int(num_of_groups)
    
    def _open_excel(self,xls_file):
        data = xlrd.open_workbook(xls_file)
        return data
                    
    def _parse_genenames(self,namefile,by_idx = 0):
        data = self._open_excel(namefile)
        table = data.sheets()[by_idx]
        namecol = table.col_values(0)
        all_names = [i for i in namecol[1:] if i]
        return all_names
            
    def _parse_conflicts_pairs(self,conflicts_file):
        data = self._open_excel(conflicts_file)
        table = data.sheets()[0]
        nrows = table.nrows
        conflicts_pairs = set()
            
        for i in range(1,nrows):
            row = table.row_values(i)
            conflicts_pairs.add((row[0],row[1]))
        return conflicts_pairs

    def _rand_group(self, namelist, num):
        count = len(namelist)
        rand_idx = range(count)
        random.shuffle(rand_idx) 
        rand_list = [namelist[i] for i in rand_idx] #throw the input list into confusion 
        distance = count/num + 1
        current_pt = 0
        grouped = []
        #split the intermingled list into several sublist
        for i in range(num):
            end_pt = current_pt + distance
            if end_pt < count:
                sub_list = rand_list[current_pt:end_pt]
                grouped.append(sub_list)
            else: 
                sub_list = rand_list[current_pt:]
                grouped.append(sub_list)
            current_pt = end_pt
        return grouped

    def _sub_two(self, grouping_list):
        #genetate all of the subset with two elements for all of the sublist
        subset = set()
        for list in grouping_list:
            count = len(list)
            for i in range(count):
                for j in range(i+1,count):
                    subset.add((list[i],list[j]))
        return subset

    def _result_save(self, li_list):
        outfile = "grouping_for_%d.xls" %self.num_of_groups
        outhandle = open(outfile, 'w')
        num = 1
        for i in li_list:
            line = '\t'.join(i)
            group = "group %d" % num
            outhandle.write(group + '\t' + line + '\n')
            num += 1

    def run(self):
        name_list = self._parse_genenames(self.namefile)
        conflicts = self._parse_conflicts_pairs(self.conflicts_file)
        
        notDone = True
        times = 0
        while notDone:
            times += 1
            print "grouping for %dth time..." % times
            #self.textEdit.append("grouping for %dth time..." % times)
            grouped_list = self._rand_group(name_list, self.num_of_groups)
            subset = self._sub_two(grouped_list)
            if not subset & conflicts: #if the subset does not have intersection with the conflicts, then we get what we want
                notDone = False
        #print grouped_list
        #print notDone
        self._result_save(grouped_list)
        
    
if __name__ == "__main__":

    namefile = sys.argv[1]
    conflicts_file = sys.argv[2]
    num_of_groups = sys.argv[3]

    job = run_grouping(namefile, conflicts_file, num_of_groups)
    job.run()
