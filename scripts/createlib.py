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

effect_hidden = kicad_sym.TextEffect(sizex=0, sizey=0, is_hidden=True)
effect_halign_left = kicad_sym.TextEffect(sizex=1.27, sizey=1.27, h_justify="left")
color_none = kicad_sym.Color(r=0, g=0, b=0, a=0)

# HACK!
lib_version = 20211014


def append_parts(lib_object, description_value_re, part_prefix, reference, footprint, symbol_pins, symbol_rectangles, where_clause):
    lib_object.version = lib_version
    cursor = conn.cursor()
    cursor.execute('select "LCSC Part", "Manufacturer", "MFR.Part", "Description", "Datasheet" from parts where {}'.format(where_clause))
    for row in cursor.fetchall():
        (lcsc_part, mfg_name, mfg_part, description, datasheet) = row
        try:
            print(description)
            m = re.match(description_value_re, description)
            print(part_prefix)
            name = m.expand(part_prefix)
            print(name)
        except:
            print("Can't parse, skipping " + lcsc_part + " '" + description + "'")
            continue
        # print(lcsc_part + " " + description)
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
    lib_object.write()
    
conn = sqlite3.connect('build/parts-basic.db');

# resistors


symbol_pins = [ kicad_sym.Pin(name="~", number="1", etype="passive", posx=0, posy=2.54, rotation=270, length=0.762, name_effect=effect_hidden, number_effect=effect_hidden),
                kicad_sym.Pin(name="~", number="2", etype="passive", posx=0, posy=-2.54, rotation=90, length=0.762, name_effect=effect_hidden, number_effect=effect_hidden),
                ]

resistor_rectangles = [ kicad_sym.Rectangle(startx=-0.762, starty=1.778, endx=0.762, endy=-1.778, fill_type="none", stroke_width=0.2032) ]

# ===========================================================================================================================
# All Resistors
lib_resistors_all = kicad_sym.KicadLibrary("build/jlcpcb-basic-resistor.kicad_sym")
append_parts(lib_resistors_all,
             ".*¡æ\s*(.*)¦¸.*",
             'R_0402_\\1',
             'R',
             'R_0402_1005Metric',
             symbol_pins,
             resistor_rectangles,
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%402"')
append_parts(lib_resistors_all,
             ".*¡æ\s*(.*)¦¸.*",
             'R_0603_\\1',
             'R',
             'R_0603_1608Metric',
             symbol_pins,
             resistor_rectangles,
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%603"')
append_parts(lib_resistors_all,
             ".*¡æ\s*(.*)¦¸.*",
             'R_0805_\\1',
             'R',
             'R_0805_2012Metric',
             symbol_pins,
             resistor_rectangles,
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%805"')
append_parts(lib_resistors_all,
             ".*¡æ\s*(.*)¦¸.*",
             'R_1206_\\1',
             'R',
             'R_1206_3216Metric',
             symbol_pins,
             resistor_rectangles,
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%1206"')

# ===========================================================================================================================
# 0402 resistors
append_parts(kicad_sym.KicadLibrary("build/jlcpcb-basic-resistor-0402.kicad_sym"),
             ".*¡æ\s*(.*)¦¸.*",
             '\\1',
             'R',
             'R_0402_1005Metric',
             symbol_pins,
             resistor_rectangles,
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%402"')

# ===========================================================================================================================
# 0603 resistors
append_parts(kicad_sym.KicadLibrary("build/jlcpcb-basic-resistor-0603.kicad_sym"),
             ".*¡æ\s*(.*)¦¸.*",
             '\\1',
             'R',
             'R_0603_1608Metric',
             symbol_pins,
             resistor_rectangles,
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%603"')

# ===========================================================================================================================
# 0805 resistors
append_parts(kicad_sym.KicadLibrary("build/jlcpcb-basic-resistor-0805.kicad_sym"),
             ".*¡æ\s*(.*)¦¸.*",
             '\\1',
             'R',
             'R_0805_2012Metric',
             symbol_pins,
             resistor_rectangles,
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%805"')

# ===========================================================================================================================
# 1206 resistors
append_parts(kicad_sym.KicadLibrary("build/jlcpcb-basic-resistor-1206.kicad_sym"),
             ".*¡æ\s*(.*)¦¸.*",
             '\\1',
             'R',
             'R_1206_3216Metric',
             symbol_pins,
             resistor_rectangles,
            '"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "1206"')

# ===========================================================================================================================
# All Capacitors
lib_capacitors_all = kicad_sym.KicadLibrary("build/jlcpcb-basic-capacitor.kicad_sym")
append_parts(lib_capacitors_all,
             "(.+)\s(.+)\s(.+)¡À.*",
             'C_0402_\\2_\\1_\\3',
             'C',
             'C_0402_1005Metric',
             symbol_pins,
             resistor_rectangles,
             '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%402"')
append_parts(lib_capacitors_all,
             "(.+)\s(.+)\s(.+)¡À.*",
             'C_0603_\\2_\\1_\\3',
             'C',
             'C_0603_1608Metric',
             symbol_pins,
             resistor_rectangles,
             '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%603"')
append_parts(lib_capacitors_all,
             "(.+)\s(.+)\s(.+)¡À.*",
             'C_0805_\\2_\\1_\\3',
             'C',
             'C_0805_2012Metric',
             symbol_pins,
             resistor_rectangles,
             '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%805"')
append_parts(lib_capacitors_all,
             "(.+)\s(.+)\s(.+)¡À.*",
             'C_1206_\\2_\\1_\\3',
             'C',
             'C_1206_3216Metric',
             symbol_pins,
             resistor_rectangles,
             '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "1206"')
sys.exit(0)

# LEDs

append_parts(lib_capacitors_all,
             ".*¡æ.* (a-zA-z) .*",
            'D_0603',
            lib_template_led,
            'LED_0603_1608Metric',
            '"Second Category" = "Light Emitting Diodes (LED)" and "Package" like "%LED_0603"')
append_parts(lib_capacitors_all,
             ".*¡æ.* (a-zA-z) .*",
            'D_0805',
            lib_template_led,
            'LED_0805_2012Metric',
            '"Second Category" = "Light Emitting Diodes (LED)" and "Package" like "%LED_0805"')

conn.close()

# select "LCSC Part", "Manufacturer", "MFR.Part", "Description", "Datasheet"  from parts where "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" = "0402";
