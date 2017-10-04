#!/usr/bin/python3

#import data

'''

formats:
xxx xxx xxxx
xxx-xxx-xxxx
xxxxxxxxxx


'''



str_nums = [
   'zero',
   'one',
   'two',
   'three',
   'four',
   'five',
   'six',
   'seven',
   'eight',
   'nine'
]


def isalpha(n):
   return n.isalpha()
def isdigit(n):
   return n.isdigit()


def try_get_num(s, n):
   s = s.lower()

   c = s[n]
   if c in ['①', '➊', '❶', '¹']:
      return (1, 1)
   if c in ['➋', '❷', '②']:
      return (2, 1)
   if c == '③':
      return (3, 1)
   if c in ['➍', '④']:
      return (4, 1)
   if c == '⑤':
      return (5, 1)
   if c in ['⑥']:
      return (6, 1)
   if c in ['⑦', '➆']:
      return (7, 1)
   if c == '⑨':
      return (9, 1)
   if c == '💯':
      return (100, 1)


   all_nums1 = "0➊➋➌➍➎➏➐➑➒➓"
   all_nums2 = "0⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾";
   for i, x in enumerate(all_nums1):
      if c == x:
         return (i, 1)

   for i, x in enumerate(all_nums2):
      if c == x:
         return (i, 1)
      pass #end for loop

   if s[n].isdigit():
      try:
         return (int(s[n]), 1)
      except Exception as e:
         pass
      pass #end if

   for i, check1 in enumerate(str_nums):
      check2 = s[n:n+len(check1)]
      if check1 == check2:
         return (i, len(check1))
      pass #endfor

   return (None, None)


def parse_phone(s, start_in=None):
   #if start_in is not None:
   #   s = s[start_in:]

   needed_num = 10
   curr_num = 0
   nums = []
   len_since_last_num = -1

   start_i = 0
   end_i = 0

   i = 0
   if start_in is not None:
      i = start_in
   while i < len(s):

      n, n_len = try_get_num(s, i)

      if len_since_last_num > 2:
         curr_num = 0
         nums = []


      #if n is None: #or part is for numbers like this: 1 1 742-323-4322
      if n is None or (len(nums) == 0 and n == 1):
         i += 1
         if len_since_last_num != -1:
            len_since_last_num += 1

      else:
         i += n_len

         nums.append(n)
         len_since_last_num = 0
         if curr_num == 0:
            start_i = i
         curr_num += 1


         if curr_num == 10:

            end_i = i
            ret1 = ''.join(map(lambda x: str(x), nums))
            return (ret1, start_i, end_i + n_len)


   return None


def get_all_nums(s):
   '''Get all phone numbers from given text'''
   nums = []

   x = parse_phone(s)
   while x is not None:
      num, start, end = x

      #print(x)
      nums.append(num)
      x = parse_phone(s, end)

   return nums

def test():
   for x, y in zip(data.test_phone_strs, data.test_expected_strs):

      #print(parse_phone(x))
      all_nums = get_all_nums(x)

      print('line: ' + x)
      print('\tphones:\t\t', all_nums)
      print('\texpected:\t', y)
      assert(all_nums == y)

   pass #end test

#test()


