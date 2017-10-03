#!/bin/bash

rm -R build
rm -r source/autoapidoc build/html
#sphinx-apidoc -o source/autoapidoc ..

cd source; ln -s ../../*py .; cd ..
sphinx-apidoc -o source/autoapidoc ..

#sphinx-apidoc -o .. ..

make html
#rm -r /sec/web/tmp/dbt_docs_acc
#mv build/html/ /sec/web/tmp/dbt_docs_acc/


dbutil_doc_path=/sec/web-static/docs/utiltools/dbutils
mkdir -p $dbutil_doc_path

cp -R build/html $dbutil_doc_path
