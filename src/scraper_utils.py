import os
from utiltools import shellutils as shu
import csv
import itertools, functools


def read_csv(fpath, is_dict=False, ignore_first_col=False):
   '''Read CSV file as list or dict'''

   with open(fpath, 'r') as csvf:
      reader_args = {'delimiter':',', 'quotechar':'"'}
      reader = csv.DictReader(csvf, **reader_args) if is_dict else csv.reader(csvf, **reader_args)
      return [row for row in reader]
   return None

def get_file_exts(path, good_exts=[]):
   '''
      good_exts=['csv', 'pdf']
   '''
   #good_fnames = list(filter(lambda fname: fname.split('.')[-1] in good_exts, shu.ls(path)))

   good_fnames = []
   for fname in shu.ls(path):
      if os.path.splitext(fname)[1].lower() in map(lambda x: '.' + x, good_exts):
         good_fnames.append(fname)

   return good_fnames



def find_index(lst, test_func):
   '''like index, except takesa a predicate function test_func'''
   for i, el in enumerate(lst):
      if test_func(el):
         return i
   return None

def str_replace_lst(string, sub_lst):
   '''Examples:
      'hello world'.replace('hello', '').replace('world', '-') -> ' -'
      str_replace_lst('hello world', [('hello', ''), ('world', '-')]) -> ' -'
      str_replace_lst('hello world', [('hello', 'bye'), ('world', 'mars')]) -> 'bye mars'
   '''

   return functools.reduce(lambda acc, val: acc.replace(val[0], val[1]), sub_lst, string)

