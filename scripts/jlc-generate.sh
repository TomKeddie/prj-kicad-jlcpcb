#!/usr/bin/env bash

mkdir -p build
[ -f build/parts.xls ] || wget -O build/parts.xls https://jlcpcb.com/componentSearch/uploadComponentInfo
[ -f build/parts.csv ] || ssconvert build/parts.xls build/parts.csv
[ -f build/createdb.sql ] || cat >build/createdb.sql <<EOF
.mode csv
.import build/parts.csv parts
create index package on parts(Package);
create index description on parts(Description);
create index category_package on parts("Second Category", "Package");
update parts set description='25V 10uF X5R ¡À20% 0603 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS' where description='X5R 25V ¡À20% 10uF 0603 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS'
update parts set description='25V 10uF X5R ¡À10% 0805 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS' where description='X5R 25V ¡À10% 10uF 0805 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS'
update parts set description='25V 22uF X5R ¡À20% 0805 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS' where description='X5R 25V ¡À20% 22uF 0805 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS'
EOF
[ -f build/createdb-basic.sql ] || cat >build/createdb-basic.sql <<EOF
.mode csv
.import build/parts.csv parts
DELETE from parts where "Library Type" <> "Basic";
create index package on parts(Package);
create index description on parts(Description);
create index category_package on parts("Second Category", "Package");
update parts set description='25V 10uF X5R ¡À20% 0603 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS' where description='X5R 25V ¡À20% 10uF 0603 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS'
update parts set description='25V 10uF X5R ¡À10% 0805 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS' where description='X5R 25V ¡À10% 10uF 0805 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS'
update parts set description='25V 22uF X5R ¡À20% 0805 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS' where description='X5R 25V ¡À20% 22uF 0805 Multilayer Ceramic Capacitors MLCC - SMD/SMT ROHS'
EOF

[ -f build/parts-basic.db ] || cat build/createdb-basic.sql | sqlite3 build/parts-basic.db
[ -f build/parts.db ] || cat build/createdb.sql | sqlite3 build/parts.db
python createlib.py
mv build/*.kicad_sym ../libraries
