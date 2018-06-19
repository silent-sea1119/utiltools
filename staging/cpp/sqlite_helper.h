#ifndef SQLITE_HELPER_H
#define SQLITE_HELPER_H

#include "faex/gdax/importer_csrc/config.h"
#include "utils.h"

#include <SQLiteCpp/SQLiteCpp.h>


#define DEFAULT_DB_FLAGS (SQLite::OPEN_READWRITE|SQLite::OPEN_CREATE)


struct table_layout_info {
   //pair<vec_str, vec_str>
   vector<uint8_t> allow_empty_col; //allowed to have empty??
   string table_name;
   vec_str* col_names;
   vec_str* col_types;
};


inline table_layout_info*
make_new_layout()
{

   table_layout_info* tli = new table_layout_info;
   tli->col_names = new vec_str;
   tli->col_types = new vec_str;

   return tli;
}


/*old
template <class T>
struct table_layout_info1 {
   //pair<vec_str, vec_str>
   string table_name;
   vec_str* col_names;
   vector<T>* col_types;
   vec<uint8_t> allow_empty_cols; //allowed to have empty??


   table_layout_info() {
      this->col_names = new vec_str;
      this->col_types = new vector<T>;
   }
};
*/

/** SQLite row binder for generic number of arguments **/
//KK Statement bind
#define KKS_BIND(stmt_p, row, n) stmt_p->bind(n+1, std::get<n>(row))

template<class T, int I>
struct RowBinder {};

template<class T>
struct RowBinder<T, 1> {
   static void bind_row(SQLite::Statement* s, T& row) {
      //BIND_ROW_FUNC_HELPER(s, row, 1);
      KKS_BIND(s, row, 0);
   }
};

template<class T>
struct RowBinder<T, 2> {
   static void bind_row(SQLite::Statement* s, T& row) {
      KKS_BIND(s, row, 0);
      KKS_BIND(s, row, 1);
   }
};


template<class T>
struct RowBinder<T, 3> {
   static void bind_row(SQLite::Statement* s, T& row) {
      KKS_BIND(s, row, 0);
      KKS_BIND(s, row, 1);
      KKS_BIND(s, row, 2);
   }
};

template<class T>
struct RowBinder<T, 4> {
   static void bind_row(SQLite::Statement* s, T& row) {
      KKS_BIND(s, row, 0);
      KKS_BIND(s, row, 1);
      KKS_BIND(s, row, 2);
      KKS_BIND(s, row, 3);
   }
};

template<class T>
struct RowBinder<T, 5> {
   static void bind_row(SQLite::Statement* s, T& row) {
      KKS_BIND(s, row, 0);
      KKS_BIND(s, row, 1);
      KKS_BIND(s, row, 2);
      KKS_BIND(s, row, 3);
      KKS_BIND(s, row, 4);
   }
};

template<class T>
struct RowBinder<T, 6> {
   static void bind_row(SQLite::Statement* s, T& row) {
      KKS_BIND(s, row, 0);
      KKS_BIND(s, row, 1);
      KKS_BIND(s, row, 2);
      KKS_BIND(s, row, 3);
      KKS_BIND(s, row, 4);
      KKS_BIND(s, row, 5);
   }
};

template<class T>
struct RowBinder<T, 7> {
   static void bind_row(SQLite::Statement* s, T& row) {
      KKS_BIND(s, row, 0);
      KKS_BIND(s, row, 1);
      KKS_BIND(s, row, 2);
      KKS_BIND(s, row, 3);
      KKS_BIND(s, row, 4);
      KKS_BIND(s, row, 5);
      KKS_BIND(s, row, 6);
   }
};

template<class T>
struct RowBinder<T, 8> {
   static void bind_row(SQLite::Statement* s, T& row) {
      KKS_BIND(s, row, 0);
      KKS_BIND(s, row, 1);
      KKS_BIND(s, row, 2);
      KKS_BIND(s, row, 3);
      KKS_BIND(s, row, 4);
      KKS_BIND(s, row, 5);
      KKS_BIND(s, row, 6);
      KKS_BIND(s, row, 7);
   }
};



/** END SQLite row binder for generic number of arguments **/


struct DbManager {

   string db_path;

   SQLite::Database sqli_db;
   map<string, table_layout_info*> table_layouts;

   SQLite::Transaction* transact;

   DbManager(string db_path_)
      : db_path(db_path_)
      , sqli_db(db_path_, DEFAULT_DB_FLAGS)
      , transact(NULL)
   {

#if PRINT_SQL_DEBUG_QUERY
	cout << "sqlite_helper.h: database: " << db_path << endl;
#endif

   }


   table_layout_info*
   get_table_layout_info(string table_name)
   {
      auto ret = this->table_layouts.find(table_name);
      if (ret == this->table_layouts.end())
         return NULL;
      return ret->second;
   }

   void createTable(table_layout_info& tli,
                    bool delete_if_exists=false,
                    bool create_if_not_exists=false)
   {
      string table_name = tli.table_name;
      vec_str* col_names = tli.col_names;
      vec_str* col_types = tli.col_types;

      assert(col_names->size() == col_types->size());

      this->table_layouts[table_name] = &tli;

      if (delete_if_exists) {
         string q = "DROP TABLE IF EXISTS " + table_name;
         this->sqli_db.exec(q);
      }

      string q = "CREATE TABLE ";

      if (create_if_not_exists)
         q += " IF NOT EXISTS ";

      q +=  table_name + " (";

      int max_index = col_names->size()-1;
      for (int i = 0; i < max_index; i++) {
         string col_name = (*col_names)[i];
         string col_type = (*col_types)[i];

         q += col_name + " " + col_type + ", ";
      }

      q += (*col_names)[max_index] + " " + (*col_types)[max_index] + ")";


#if PRINT_SQL_DEBUG_QUERY
	cout << "create command: " << q << endl;
#endif

      this->sqli_db.exec(q);

   }


   void free_table_layouts() {

	for (auto x : this->table_layouts) {
	   table_layout_info* li = x.second;

	   delete li->col_names;
	   delete li->col_types;
	   delete li;
	}

   }


   SQLite::Transaction* transact_new() {
      this->transact = new SQLite::Transaction(this->sqli_db);
      return this->transact;
   }

   void transact_commit_free() {
      this->transact->commit();
      delete this->transact;
   }

   template <class T, int I> //Tuple
   bool insertMany(string table_name, vector<T> data, bool new_transact=true)
   {

#if PRINT_SQL_DEBUG_QUERY
      DEBUG_PRINT("insert many " + table_name);
#endif

	//assert(data.size() > 0);
      if (data.size() == 0)
         return false;


      table_layout_info* t = this->get_table_layout_info(table_name);
	size_t num_cols_first_row = std::tuple_size<T>::value;
      size_t num_cols_table_info = t->col_names->size();
      assert(t != NULL && num_cols_first_row == num_cols_table_info);

      string q;
	q = "INSERT INTO " + table_name + " VALUES (";

      for (uint32_t i = 0; i < num_cols_first_row; i++) {
         if (i != 0)
            q += ", ";
         q += "?";
      }
      q += ")";


#if PRINT_SQL_DEBUG_QUERY
      cout << "db path: " << this->db_path << endl;
	cout << "insert command: " << q << endl;
#endif

      if (new_transact)
         this->transact_new();

      SQLite::Statement insert_stmt(this->sqli_db, q);

	for (auto row : data) {

         insert_stmt.reset();

         bool is_v1 = false;

         if (is_v1) { //v1
            int i = 1;
            for_each_in_tuple(row, [&i, &insert_stmt](const auto &col_val) {
               insert_stmt.bind(i, col_val);
               i += 1;
            });
         }
         else { //v2
            RowBinder<T, I>::bind_row(&insert_stmt, row);
         }


         insert_stmt.exec();
	}

      if (new_transact)
         this->transact_commit_free();

#if PRINT_SQL_DEBUG_QUERY
      DEBUG_PRINT("end insert many");
#endif

      //throw "hi";

      return true;

   }



   template <class T>
   bool insertManyVec(string table_name, vector<vector<T>> data) { return false; }

   template <class T>
   void insertSingleRow(string table_name,
                        vector<T> data)
   {}

};


inline DbManager*
init_db(string db_path) {

   DbManager* m;

   try {
      m = new DbManager(db_path);
   }
   catch (const std::exception& e) {
      cout << "failure to open SQLite db ("
           << db_path << "): " << e.what();
      return NULL;
   }
   return m;

}


#endif //SQLITE_HELPER_H
