#!/usr/bin/env python3
import sqlite3
import re
import operator
import sys

lib_header = ''''''

lib_footer = ''''''

lib_template_resistor = ''' name "{}" value "{}" footprint "{}" datasheet "{}" description "{}" lcsc "{}" 
'''

lib_template_capacitor = lib_template_resistor
lib_template_led = lib_template_resistor

def append_parts(lib_file, description_value_re, part_prefix, lib_template, kicad_footprint, where_clause):
    cursor = conn.cursor()
    cursor.execute('select "LCSC Part", "Manufacturer", "MFR.Part", "Description", "Datasheet" from parts where {}'.format(where_clause))
    for row in cursor.fetchall():
        (lcsc_part, mfg_name, mfg_part, description, datasheet) = row
        try:
            m = re.match(description_value_re, description)
            value = m.group(1).strip()
        except:
            print("Can't parse, skipping " + lcsc_part + " '" + description + "'")
            continue
        # print(lcsc_part + " " + description)
        name = part_prefix + "_" + value
        description_txt =  mfg_name + "," + mfg_part + "," + re.sub("[^-A-Za-z 0-9%(),]", " ", description)
        lib_file.write(lib_template.format(name, value, kicad_footprint, datasheet, description_txt, lcsc_part))
    
conn = sqlite3.connect('build/parts-basic.db');

# resistors

lib_file = open('build/jlcpcb-basic-resistor.kicad_sym', 'w')
lib_0402_file = open('build/jlcpcb-basic-resistor-0402.kicad_sym', 'w')
lib_0603_file = open('build/jlcpcb-basic-resistor-0603.kicad_sym', 'w')
lib_0805_file = open('build/jlcpcb-basic-resistor-0805.kicad_sym', 'w')
lib_1206_file = open('build/jlcpcb-basic-resistor-1206.kicad_sym', 'w')

for f in [lib_file, lib_0402_file, lib_0603_file, lib_0805_file, lib_1206_file]:
    f.write(lib_header)

# "¡À1% 1/16W Thick Film Resistors 50V ¡À100ppm/¡æ -55¡æ~+155¡æ 2k¦¸ 0402 Chip Resistor - Surface Mount ROHS"
append_parts(lib_file,
             ".*¡æ(.*)¦¸.*",
            'R_0402',
            lib_template_resistor,
            'R_0402_1005Metric',
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%402"')
append_parts(lib_0402_file,
             ".*¡æ(.*)¦¸.*",
            'R',
            lib_template_resistor,
            'R_0402_1005Metric',
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%402"')

append_parts(lib_file,
             ".*¡æ(.*)¦¸.*",
            'R_0603',
            lib_template_resistor,
            'R_0603_1608Metric',
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%603"')
append_parts(lib_0603_file,
             ".*¡æ(.*)¦¸.*",
            'R',
            lib_template_resistor,
            'R_0603_1608Metric',
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%603"')

append_parts(lib_file,
             ".*¡æ(.*)¦¸.*",
            'R_0805',
            lib_template_resistor,
            'R_0805_2012Metric',
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%805"')
append_parts(lib_0805_file,
             ".*¡æ(.*)¦¸.*",
            'R',
            lib_template_resistor,
            'R_0805_2012Metric',
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%805"')

append_parts(lib_file,
             ".*¡æ(.*)¦¸.*",
            'R_1206',
            lib_template_resistor,
            'R_1206_3216Metric',
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%1206"')
append_parts(lib_1206_file,
             ".*¡æ(.*)¦¸.*",
            'R',
            lib_template_resistor,
            'R_1206_3216Metric',
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%1206"')

for f in [lib_file,
            lib_0402_file,
            lib_0603_file,
            lib_0805_file,
            lib_1206_file]:
    f.write(lib_footer)
    f.close()

# capacitors

lib_file = open('build/jlcpcb-basic-mlcc.kicad_sym', 'w')
lib_0402_file = open('build/jlcpcb-basic-mlcc-0402.kicad_sym', 'w')
lib_0603_file = open('build/jlcpcb-basic-mlcc-0603.kicad_sym', 'w')
lib_0805_file = open('build/jlcpcb-basic-mlcc-0805.kicad_sym', 'w')
lib_1206_file = open('build/jlcpcb-basic-mlcc-1206.kicad_sym', 'w')

for f in [lib_file, lib_0402_file, lib_0603_file, lib_0805_file, lib_1206_file]:
    f.write(lib_header)

append_parts(lib_file,
             "(.*)¡À.*",
            'C_0402',
            lib_template_capacitor,
            'C_0402_1005Metric',
            '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%402"')
append_parts(lib_0402_file,
             "(.*)¡À.*",
            'C',
            lib_template_capacitor,
            'C_0402_1005Metric',
            '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%402"')

append_parts(lib_file,
             "(.*)¡À.*",
            'C_0603',
            lib_template_capacitor,
            'C_0603_1608Metric',
            '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%603"')
append_parts(lib_0603_file,
             "(.*)¡À.*",
            'C',
            lib_template_capacitor,
            'C_0603_1608Metric',
            '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%603"')

append_parts(lib_file,
             "(.*)¡À.*",
            'C_0805',
            lib_template_capacitor,
            'C_0805_2012Metric',
            '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%805"')
append_parts(lib_0805_file,
             "(.*)¡À.*",
            'C',
            lib_template_capacitor,
            'C_0805_2012Metric',
            '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%805"')

append_parts(lib_file,
             "(.*)¡À.*",
            'C_1206',
            lib_template_capacitor,
            'C_1206_3216Metric',
            '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%1206"')
append_parts(lib_1206_file,
             "(.*)¡À.*",
            'C',
            lib_template_capacitor,
            'C_1206_3216Metric',
            '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%1206"')

for f in [lib_file, lib_0402_file, lib_0603_file, lib_0805_file, lib_1206_file]:
    f.write(lib_footer)
    f.close()

sys.exit(0)
# LEDs
lib_file = open('build/jlcpcb-basic-led.kicad_sym',
            'w')
lib_file.write(lib_header)
append_parts(lib_file,
             ".*¡æ.* (a-zA-z) .*",
            'D',
            lib_template_led,
            'LED_0603_1608Metric',
            '"Second Category" = "Light Emitting Diodes (LED)" and "Package" like "%LED_0603"')
append_parts(lib_file,
             ".*¡æ.* (a-zA-z) .*",
            'D',
            lib_template_led,
            'LED_0805_2012Metric',
            '"Second Category" = "Light Emitting Diodes (LED)" and "Package" like "%LED_0805"')
lib_file.write(lib_footer)
lib_file.close()


conn.close()

# select "LCSC Part", "Manufacturer", "MFR.Part", "Description", "Datasheet"  from parts where "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" = "0402";
