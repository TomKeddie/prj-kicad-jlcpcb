#!/usr/bin/env bash

mkdir -p build
[ -f build/parts.xls ] || wget -O build/parts.xls https://jlcpcb.com/componentSearch/uploadComponentInfo
[ -f build/parts.csv ] || ssconvert build/parts.xls build/parts.csv
[ -f build/createdb-basic.sql ] || cat >build/createdb-basic.sql <<EOF
.mode csv
.import build/parts.csv parts
DELETE from parts where "Library Type" <> "Basic";
create index package on parts(Package);
create index description on parts(Description);
create index category_package on parts("Second Category", "Package");
EOF
[ -f build/parts-basic.db ] || cat build/createdb-basic.sql | sqlite3 build/parts-basic.db
python createlib.py
mv build/*.lib build/*.dcm ../libraries
