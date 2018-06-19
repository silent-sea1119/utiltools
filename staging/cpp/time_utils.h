#ifndef TIME_UTILS_H_INCLUDE
#define TIME_UTILS_H_INCLUDE

#include <iostream>
#include <chrono>
#include <ctime>
#include <sys/time.h>

//#include <sstream>
//#include <locale>
//#include <iomanip>
#include <chrono>

#include <sstream>

#include "faex/gdax/lib-deps/date/include/date/tz.h"
#include "faex/gdax/lib-deps/date/include/date/date.h"


using namespace std;


inline std::chrono::microseconds
micros_from_date(const std::string& s)
{
   using namespace std::chrono;
   using sys_microseconds = time_point<system_clock, microseconds>;
   sys_microseconds pt;
   std::istringstream is(s);
   is >> date::parse("%FT%TZ", pt);
   //date::parse(is, "%FT%TZ", pt); //GODAM PIECE OF CRAP


   return pt.time_since_epoch();
}

inline std::string
date_from_micros(std::chrono::microseconds ms)
{
  using namespace std::chrono;
  using sys_microseconds = time_point<system_clock, microseconds>;
  return date::format("%FT%TZ", sys_microseconds{ms});
}

inline uint64_t convert_str_time_to_uint64(string time) {

	return micros_from_date(time).count();
   /*std::tm t = {};
   std::istringstream ss(time);

   if (ss >> std::get_time(&t, "%Y-%m%-%dT%H:%M:%S")) {
      return std::mktime(&t);

   }
   else {
      cout << "time conversion error" << endl;
      exit(-1);
   }*/
}




inline string format_time(time_t t) {
   return ctime(&t);
}

inline time_t get_time_tstamp() {
   //auto start = std::chrono::system_clock::now();
   auto start = std::chrono::high_resolution_clock::now();

   time_t start_time = std::chrono::system_clock::to_time_t(start);
   return start_time;
}

//micro seconds
inline uint64_t getMicroTstamp() {
   struct timeval tv;
   gettimeofday(&tv,NULL);
   return tv.tv_sec*(uint64_t)1000000+tv.tv_usec;
}



inline void test_time() {

   time_t start_time = get_time_tstamp();
   uint64_t micro1 = getMicroTstamp();
   uint64_t micro2 = getMicroTstamp();

   cout //<< "start tstamp " << start << endl
        << "micro1: " << micro1 << endl
        << "micro2: " << micro2 << endl
        << "start time: " << start_time << endl
        << "start time2: " << format_time(start_time); //ctime(&start_time);
}


#endif //TIME_UTILS_H_INCLUDE

