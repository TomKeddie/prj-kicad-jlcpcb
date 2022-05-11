#!/usr/bin/env python3
import sqlite3
import re
import operator
import sys
import importlib

sys.path.append("kicad_library_utils/common")

import kicad_sym

lib_header = ''''''

lib_footer = ''''''

lib_template_resistor = ''' name "{}" value "{}" footprint "{}" datasheet "{}" description "{}" lcsc "{}" 
'''

lib_template_capacitor = lib_template_resistor
lib_template_led = lib_template_resistor

effect_hidden = kicad_sym.TextEffect(sizex=0, sizey=0, is_hidden=True)
effect_halign_left = kicad_sym.TextEffect(sizex=1.27, sizey=1.27, h_justify="left")
color_none = kicad_sym.Color(r=0, g=0, b=0, a=0)

def append_parts(lib_object, description_value_re, part_prefix, lib_template, reference, footprint, symbol_pins, symbol_rectangles, where_clause):
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
        description_txt = re.sub("[^-A-Za-z 0-9%(),]", " ", description).strip()
        symbol = kicad_sym.KicadSymbol.new(name=name,
                                           libname="jlcpcb-basic-resistor",
                                           reference=reference,
                                           footprint=footprint,
                                           description=description_txt,
                                           datasheet=datasheet,
        )
        symbol.properties.append(kicad_sym.Property(name="LCSC", value=lcsc_part, idd=len(symbol.properties), effects=effect_hidden))
        symbol.properties.append(kicad_sym.Property(name="MFG", value=mfg_name, idd=len(symbol.properties), effects=effect_hidden))
        symbol.properties.append(kicad_sym.Property(name="MFGPN", value=mfg_part, idd=len(symbol.properties), effects=effect_hidden))
        symbol.get_property("Reference").posx=0.762
        symbol.get_property("Reference").posy=0.508
        symbol.get_property("Reference").effects=effect_halign_left
        symbol.get_property("Value").posx=0.762
        symbol.get_property("Value").posy=-1.016
        symbol.get_property("Value").effects=effect_halign_left
        for pin in symbol_pins:
            symbol.pins.append(pin)
        for rectangle in symbol_rectangles:
            symbol.rectangles.append(rectangle)
        lib_object.symbols.append(symbol)
    
conn = sqlite3.connect('build/parts-basic.db');

# resistors

lib_resistors_all = kicad_sym.KicadLibrary("build/jlcpcb-basic-resistor.kicad_sym")
lib_resistors_all.version = 20211014

symbol_pins = [ kicad_sym.Pin(name="~", number="1", etype="passive", posx=0, posy=2.54, rotation=270, length=0.762, name_effect=effect_hidden, number_effect=effect_hidden),
                kicad_sym.Pin(name="~", number="2", etype="passive", posx=0, posy=-2.54, rotation=90, length=0.762, name_effect=effect_hidden, number_effect=effect_hidden),
                ]

# (start -0.762 1.778) (end 0.762 -1.778)
resistor_rectangles = [ kicad_sym.Rectangle(startx=-0.762, starty=1.778, endx=0.762, endy=-1.778, fill_type="none", stroke_width=0.2032) ]

#0.762 -1.016 0

append_parts(lib_resistors_all,
             ".*¡æ(.*)¦¸.*",
             'R_0402',
             lib_template_resistor,
             'R',
             'R_0402_1005Metric',
             symbol_pins,
             resistor_rectangles,
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%402"')

lib_resistors_all.write()
sys.exit(0)


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

# capacitors

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
sys.exit(0)

# LEDs

append_parts(lib_file,
             ".*¡æ.* (a-zA-z) .*",
            'D_0603',
            lib_template_led,
            'LED_0603_1608Metric',
            '"Second Category" = "Light Emitting Diodes (LED)" and "Package" like "%LED_0603"')
append_parts(lib_file,
             ".*¡æ.* (a-zA-z) .*",
            'D_0805',
            lib_template_led,
            'LED_0805_2012Metric',
            '"Second Category" = "Light Emitting Diodes (LED)" and "Package" like "%LED_0805"')

conn.close()

# select "LCSC Part", "Manufacturer", "MFR.Part", "Description", "Datasheet"  from parts where "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" = "0402";
