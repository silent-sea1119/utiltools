#ifndef GENERIC_UTILS_H_INCLUDE
#define GENERIC_UTILS_H_INCLUDE


#include <unistd.h>
#include <iostream>
#include <vector>
#include <map>



using std::vector;
using std::string;
using std::map;
using std::endl;
using std::cout;


typedef vector<string> vec_str;
typedef const char* cstr_t;
typedef const string& c_ref_str;


template <class T>
using StrMap = map<string, T>;

#define CREF(x) const x&



#define BUFFER_FLUSH(buff, buff_len, flush_file) \
   do { \
      if (buff_len > 0) { \
         flush_file.write(buff, buff_len); \
         buff_len = 0; \
      } \
   } while (0)

#define BUFFER_ADD(buff, buff_len, new_data, new_data_len, max_buff_len, flush_file) \
   do { \
      if (new_data_len + buff_len >= max_buff_len) { \
         BUFFER_FLUSH(buff, buff_len, flush_file); \
      } \
      memcpy(buff + buff_len, new_data, new_data_len); \
      buff_len += new_data_len; \
   } while (0)



#endif //GENERIC_UTILS_H_INCLUDE
