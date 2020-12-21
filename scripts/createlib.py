#!/usr/bin/env python3
import sqlite3
import re
import operator

lib_header = '''EESchema-LIBRARY Version 2.4
#encoding utf-8'''

lib_footer = '''
#
#End Library
'''

lib_template_resistor = '''
#
# {0}
#
DEF {0} R 0 40 N N 1 F N
F0 "R" 80 0 50 V V C CNN
F1 "{1}" 0 0 50 V V C CNN
F2 "{2}" -70 0 50 V I C CNN
F3 "{3}" 0 0 50 V I C CNN
F4 "{4}" 0 0 50 V I C CNN "LCSC"
DRAW
S -30 70 30 -70 0 1 8 N
X ~ 1 0 100 30 D 50 50 1 1 P
X ~ 2 0 -100 30 U 50 50 1 1 P
ENDDRAW
ENDDEF'''

lib_template_capacitor = '''
#
# {0}
#
DEF {0} C 0 10 N N 1 F N
F0 "C" 25 100 50 H V L CNN
F1 "{1}" 25 -100 50 H V L CNN
F2 "{2}" 38 -150 50 H I C CNN
F3 "{3}" 0 0 50 V I C CNN
F4 "{4}" 0 0 50 V I C CNN "LCSC"
DRAW
P 2 0 1 20 -80 -30 80 -30 N
P 2 0 1 20 -80 30 80 30 N
X ~ 1 0 150 110 D 50 50 1 1 P
X ~ 2 0 -150 110 U 50 50 1 1 P
ENDDRAW
ENDDEF'''

lib_template_led = '''
#
# {0}
#
DEF {0} D 0 40 N N 1 F N
F0 "D"  0 100 50 H V C CNN
F1 "{1}" 0 -100 50 H V C CNN
F2 "{2}" 0 0 50 H I C CNN
F3 "{3}" 0 0 50 V I C CNN
F4 "{4}" 0 0 50 V I C CNN "LCSC"
DRAW
P 2 0 1 10 -50 -50 -50 50 N
P 2 0 1 0 -50 0 50 0 N
P 4 0 1 10 50 -50 50 50 -50 0 50 -50 N
P 5 0 1 0 -120 -30 -180 -90 -150 -90 -180 -90 -180 -60 N
P 5 0 1 0 -70 -30 -130 -90 -100 -90 -130 -90 -130 -60 N
X K 1 -150 0 100 R 50 50 1 1 P
X A 2 150 0 100 L 50 50 1 1 P
ENDDRAW
ENDDEF'''

dcm_header = '''EESchema-DOCLIB  Version 2.0
#
'''

dcm_footer = '''#
#End Doc Library'''

dcm_template = '''$CMP {0}
D {1}
F {2}
$ENDCMP
'''

def append_parts(lib_file, dcm_file, description_prefix, part_prefix, lib_template, kicad_footprint, where_clause):
    cursor = conn.cursor()
    cursor.execute('select "LCSC Part", "Manufacturer", "MFR.Part", "Package", "Description", "Datasheet" from parts where {}'.format(where_clause))
    for row in cursor.fetchall():
        (partno, mfg, mfgpart, package, description, datasheet) = row
        description = re.sub(description_prefix, '', description)
        m = re.match('(\S+).*', description)
        value = m.group(1)
        value = re.sub('MOhms', 'M', value)
        value = re.sub('KOhms', 'k', value)
        value = re.sub('Ohms', 'R', value)
        name = "{}_{}_{}".format(part_prefix, package, value)
        lib_file.write(lib_template.format(name, value, kicad_footprint, datasheet, partno))
        dcm_file.write(dcm_template.format(name, description, datasheet))
    
conn = sqlite3.connect('build/parts-basic.db');

# resistors

lib_file = open('build/jlcpcb-basic-resistor.lib', 'w')
lib_file.write(lib_header)
dcm_file = open('build/jlcpcb-basic-resistor.dcm', 'w')
dcm_file.write(dcm_header)
append_parts(lib_file, dcm_file, 'Chip Resistor - Surface Mount ', 'R', lib_template_resistor, 'R_0402_1005Metric', '"Second Category" = "Chip Resistor - Surface Mount" and "Package" = "0402"')
append_parts(lib_file, dcm_file, 'Chip Resistor - Surface Mount ', 'R', lib_template_resistor, 'R_0603_1608Metric', '"Second Category" = "Chip Resistor - Surface Mount" and "Package" = "0603"')
append_parts(lib_file, dcm_file, 'Chip Resistor - Surface Mount ', 'R', lib_template_resistor, 'R_0805_2012Metric', '"Second Category" = "Chip Resistor - Surface Mount" and "Package" = "0805"')
append_parts(lib_file, dcm_file, 'Chip Resistor - Surface Mount ', 'R', lib_template_resistor, 'R_1206_3216Metric', '"Second Category" = "Chip Resistor - Surface Mount" and "Package" = "1206"')
dcm_file.write(dcm_footer)
dcm_file.close()
lib_file.write(lib_footer)
lib_file.close()

# capacitors

lib_file = open('build/jlcpcb-basic-mlcc.lib', 'w')
lib_file.write(lib_header)
dcm_file = open('build/jlcpcb-basic-mlcc.dcm', 'w')
dcm_file.write(dcm_header)
append_parts(lib_file, dcm_file, 'Multilayer Ceramic Capacitors MLCC - SMD/SMT ', 'C', lib_template_capacitor, 'C_0402_1005Metric', '"Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" = "0402"')
append_parts(lib_file, dcm_file, 'Multilayer Ceramic Capacitors MLCC - SMD/SMT ', 'C', lib_template_capacitor, 'C_0603_1608Metric', '"Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" = "0603"')
append_parts(lib_file, dcm_file, 'Multilayer Ceramic Capacitors MLCC - SMD/SMT ', 'C', lib_template_capacitor, 'C_0805_2012Metric', '"Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" = "0805"')
append_parts(lib_file, dcm_file, 'Multilayer Ceramic Capacitors MLCC - SMD/SMT ', 'C', lib_template_capacitor, 'C_1206_3216Metric', '"Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" = "1206"')
dcm_file.write(dcm_footer)
dcm_file.close()
lib_file.write(lib_footer)
lib_file.close()

# LEDs
lib_file = open('build/jlcpcb-basic-led.lib', 'w')
lib_file.write(lib_header)
dcm_file = open('build/jlcpcb-basic-led.dcm', 'w')
dcm_file.write(dcm_header)
append_parts(lib_file, dcm_file, 'Light Emitting Diodes \(LED\) ', 'D', lib_template_led, 'LED_0603_1608Metric', '"Second Category" = "Light Emitting Diodes (LED)" and "Package" = "LED_0603"')
append_parts(lib_file, dcm_file, 'Light Emitting Diodes \(LED\) ', 'D', lib_template_led, 'LED_0805_1608Metric', '"Second Category" = "Light Emitting Diodes (LED)" and "Package" = "LED_0805"')
dcm_file.write(dcm_footer)
dcm_file.close()
lib_file.write(lib_footer)
lib_file.close()


conn.close()

# select "LCSC Part", "Manufacturer", "MFR.Part", "Description", "Datasheet"  from parts where "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" = "0402";
