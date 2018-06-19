#ifndef UTILS_H_INCLUDE
#define UTILS_H_INCLUDE

#include <fstream>
#include <utility> //for_each_in_tuple index_sequence
#include <tuple>
#include <map>
#include <string>
#include <sstream>
#include <cstdio>
#include <boost/filesystem.hpp>
#include <boost/range/iterator_range.hpp>

#include "generic_utils.h"
#include "time_utils.h"

using std::ofstream;
using std::tuple;
using std::map;


/* remove file; return whether it was successful */
inline bool rm_file(string path) {
   int ret = std::remove(path.c_str());
   return ret == 0;
}

inline vector<string> list_directories(string path_str) {
   using namespace boost::filesystem;

   path p(path_str.c_str());

   vector<string> ret;

   if (is_directory(p)) {
      for (auto entry : boost::make_iterator_range(directory_iterator(p), {})) {
         ret.push_back(entry.path().string());
      }
   }
   return ret;
}


/* HELPERS */

inline bool mkFolder(string path_str) {

	boost::filesystem::path dir_path(path_str);

	return boost::filesystem::create_directory(dir_path);
}

inline bool mkFolderRec(string path_str) {

	boost::filesystem::path dir_path(path_str);

	return boost::filesystem::create_directories(dir_path);
}

/* END HELPERS */

inline bool file_exists(string fname) {
   return boost::filesystem::exists(fname.c_str());
}


inline bool
read_file_whole(string fname, string** ret)
{

   if (!file_exists(fname)) {
      return false;
   }

   std::ifstream t(fname);
   std::string* str = new string;

   t.seekg(0, std::ios::end);
   str->reserve(t.tellg());
   t.seekg(0, std::ios::beg);


   str->assign((std::istreambuf_iterator<char>(t)),
                    std::istreambuf_iterator<char>());

   *ret = str;
   return ret;
}

inline bool
read_file(string fname, vector<string>* lines)
{
   if (!file_exists(fname)) {
      return false;
   }

   try {
      std::ifstream infile(fname.c_str());
      string line;

      std::ostringstream oss;

      while (std::getline(infile, line)) {

          // process pair (a,b)
          lines->push_back(line);


          /*std::istringstream iss(line);
          int a, b;
          if (!(iss >> a >> b))
            break; //error
         */
      }
      return true;
   }
   catch (std::exception& e) {
      cout << "failed reading file " << fname << endl;
      cout << e.what() << endl;
      return false;
   }
}


inline void
write_file(string path, string val) {
   ofstream myf;
   myf.open(path);
   myf << val;
   myf.close();
}



class Logger {
   FILE* log_f;
   string log_fname;
   int log_level_stdout;
public:

   Logger(string log_fname_, int log_level_stdout_)
      : log_fname(log_fname_), log_level_stdout(log_level_stdout_)
   {}

   void log(int level, string msg) {
      cout << endl << "log lvl: " << level << msg;
   }

};



#include "faex/gdax/lib-deps/json.hpp"
using json = nlohmann::json;
typedef json::iterator jit;

inline vector<string>
get_json_keys(json j) {
   vector<string> ret;

   for (jit it = j.begin(); it != j.end(); ++it) {
      ret.push_back(it.key());
   }
   return ret;
}



inline vector<string> get_json_keys(json& j) {

   vector<string> ret;

   for (json::iterator it = j.begin(); it != j.end(); ++it) {
      string key = it.key();
      ret.push_back(it.key());
   }

   return ret;
}


inline void
print_str_vec(vector<string> vec_str) {

   string print_str = "[";
   bool first = true;
   for (auto x : vec_str) {
      if (!first)
         print_str += ", ";
      first = false;

      print_str += "'" + x + "'";
   }

   print_str += "]";

   cout << print_str << endl;
}


#define DEBUG_PRINT(x) do { \
   cout << x << endl; \
} while (0)


template<class F, class...Ts, std::size_t...Is>
inline void for_each_in_tuple(const std::tuple<Ts...> & tuple, F func, std::index_sequence<Is...>){
    using expander = int[];
    (void)expander { 0, ((void)func(std::get<Is>(tuple)), 0)... };
}

template<class F, class...Ts>
inline void for_each_in_tuple(const std::tuple<Ts...> & tuple, F func){
    for_each_in_tuple(tuple, func, std::make_index_sequence<sizeof...(Ts)>());
}

/*
auto some = std::make_tuple("I am good", 255, 2.1);
for_each_in_tuple(some, [](const auto &x) { std::cout << x << std::endl; });
*/




#include <boost/algorithm/string/classification.hpp> // Include boost::for is_any_of
#include <boost/algorithm/string/split.hpp> // Include for boost::split

inline vec_str split_str(string s, string split_by) {
   vec_str ret;

   using boost::split;
   using boost::is_any_of;
   using boost::token_compress_on;

   split(ret, s, is_any_of(split_by), token_compress_on);
   return ret;
}

/*
#include <string>
#include <sstream>
#include <vector>
#include <iterator>

template<typename Out>
void split(const std::string &s, char delim, Out result) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        *(result++) = item;
    }
}

std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, std::back_inserter(elems));
    return elems;
}*/


template <class T>
inline bool contains(vector<T>& v, T& elem) {
   auto ret = std::find(v.begin(), v.end(), elem);

   return ret != v.end();
}


template <class T>
inline int get_item_index(CREF(vector<T>) elems, CREF(T) elem) {
   auto it = std::find(elems.begin(), elems.end(), elem);
   if (it == elems.end())
	return -1;
   else
	return std::distance(elems.begin(), it);
}


inline string replaceChar(string s, char c1, char c2) {

   string ret = "";

   for (uint32_t i = 0; i < s.length(); i++) {
      if (s[i] == c1)
         ret += c2;
      else
         ret += s[i];
   }
   return ret;
}


#endif // UTILS_H_INCLUDE

