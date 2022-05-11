#!/usr/bin/env python3
import sqlite3
import re
import operator
import sys
import importlib

sys.path.append("kicad_library_utils/common")

import kicad_sym

effect_hidden      = kicad_sym.TextEffect(sizex=0, sizey=0, is_hidden=True)
effect_halign_left = kicad_sym.TextEffect(sizex=1.27, sizey=1.27, h_justify="left")
color_none         = kicad_sym.Color(r=0, g=0, b=0, a=0)

# HACK!
lib_version = 20211014


def append_parts(lib_object, description_value_re, name_expand_template, reference, footprint, where_clause, symbol_pins, text_posx, value_expand_template=None, symbol_rectangles=None, symbol_polylines=None):
    lib_object.version = lib_version
    cursor = conn.cursor()
    cursor.execute('select "LCSC Part", "Manufacturer", "MFR.Part", "Description", "Datasheet" from parts where {}'.format(where_clause))
    for row in cursor.fetchall():
        (lcsc_part, mfg_name, mfg_part, description, datasheet) = row
        try:
            m = re.match(description_value_re, description)
            name = m.expand(name_expand_template)
            if value_expand_template:
                value = m.expand(value_expand_template)
            else:
                value = name
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
        symbol.get_property("Reference").posx=text_posx
        symbol.get_property("Reference").posy=0.508
        symbol.get_property("Reference").effects=effect_halign_left
        symbol.get_property("Value").value=value
        symbol.get_property("Value").posx=text_posx
        symbol.get_property("Value").posy=-1.016
        symbol.get_property("Value").effects=effect_halign_left
        for pin in symbol_pins:
            symbol.pins.append(pin)
        if symbol_rectangles:
            for rectangle in symbol_rectangles:
                symbol.rectangles.append(rectangle)
        if symbol_polylines:
            for polyline in symbol_polylines:
                symbol.polylines.append(polyline)
        lib_object.symbols.append(symbol)
    lib_object.write()
    
conn = sqlite3.connect('build/parts-basic.db');

# resistors


resistor_pins = [ kicad_sym.Pin(name="~", number="1", etype="passive", posx=0, posy=2.54, rotation=270, length=0.762, name_effect=effect_hidden, number_effect=effect_hidden),
                kicad_sym.Pin(name="~", number="2", etype="passive", posx=0, posy=-2.54, rotation=90, length=0.762, name_effect=effect_hidden, number_effect=effect_hidden),
]
resistor_rectangles = [ kicad_sym.Rectangle(startx=-0.762, starty=1.778, endx=0.762, endy=-1.778, fill_type="none", stroke_width=0.2032)
]

capacitor_pins = [ kicad_sym.Pin(name="~", number="1", etype="passive", posx=0, posy=2.54, rotation=270, length=2.032, name_effect=effect_hidden, number_effect=effect_hidden),
                   kicad_sym.Pin(name="~", number="2", etype="passive", posx=0, posy=-2.54, rotation=90, length=2.032, name_effect=effect_hidden, number_effect=effect_hidden),
]
capacitor_polylines = [ kicad_sym.Polyline(points=[kicad_sym.Point(x=-1.524, y=-0.508), kicad_sym.Point(x=1.524, y=-0.508) ], stroke_width=0.3048),
                        kicad_sym.Polyline(points=[kicad_sym.Point(x=-1.524, y=+0.508), kicad_sym.Point(x=1.524, y=+0.508) ], stroke_width=0.3048),
]

# ===========================================================================================================================
# All Resistors
lib_resistors_all = kicad_sym.KicadLibrary("build/jlcpcb-basic-resistor.kicad_sym")
append_parts(lib_object=lib_resistors_all,
             description_value_re="¡À([0-9%]+).*¡æ\s*(.*)¦¸.*",
             name_expand_template='0402_\\2',
             value_expand_template='\\2/\\1',
             reference='R',
             footprint='R_0402_1005Metric',
             symbol_pins=resistor_pins,
             symbol_rectangles=resistor_rectangles,
             text_posx=0.762,
             where_clause='"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%402"')
append_parts(lib_object=lib_resistors_all,
             description_value_re="¡À([0-9%]+).*¡æ\s*(.*)¦¸.*",
             name_expand_template='0603_\\2',
             value_expand_template='\\2/\\1',
             reference='R',
             footprint='R_0603_1608Metric',
             symbol_pins=resistor_pins,
             symbol_rectangles=resistor_rectangles,
             text_posx=0.762,
             where_clause='"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%603"')
append_parts(lib_object=lib_resistors_all,
             description_value_re="¡À([0-9%]+).*¡æ\s*(.*)¦¸.*",
             name_expand_template='0805_\\2',
             value_expand_template='\\2/\\1',
             reference='R',
             footprint='R_0805_2012Metric',
             symbol_pins=resistor_pins,
             symbol_rectangles=resistor_rectangles,
             text_posx=0.762,
             where_clause='"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%805"')
append_parts(lib_object=lib_resistors_all,
             description_value_re="¡À([0-9%]+).*¡æ\s*(.*)¦¸.*",
             name_expand_template='1206_\\2',
             value_expand_template='\\2/\\1',
             reference='R',
             footprint='R_1206_3216Metric',
             symbol_pins=resistor_pins,
             symbol_rectangles=resistor_rectangles,
             text_posx=0.762,
             where_clause='"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%1206"')

# ===========================================================================================================================
# 0402 resistors
append_parts(lib_object=kicad_sym.KicadLibrary("build/jlcpcb-basic-resistor-0402.kicad_sym"),
             description_value_re="¡À([0-9%]+).*¡æ\s*(.*)¦¸.*",
             name_expand_template='\\2',
             value_expand_template='\\2/\\1',
             reference='R',
             footprint='R_0402_1005Metric',
             symbol_pins=resistor_pins,
             symbol_rectangles=resistor_rectangles,
             text_posx=0.762,
             where_clause='"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%402"')

# ===========================================================================================================================
# 0603 resistors
append_parts(lib_object=kicad_sym.KicadLibrary("build/jlcpcb-basic-resistor-0603.kicad_sym"),
             description_value_re="¡À([0-9%]+).*¡æ\s*(.*)¦¸.*",
             name_expand_template='\\2',
             value_expand_template='\\2/\\1',
             reference='R',
             footprint='R_0603_1608Metric',
             symbol_pins=resistor_pins,
             symbol_rectangles=resistor_rectangles,
             text_posx=0.762,
             where_clause='"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%603"')

# ===========================================================================================================================
# 0805 resistors
append_parts(lib_object=kicad_sym.KicadLibrary("build/jlcpcb-basic-resistor-0805.kicad_sym"),
             description_value_re="¡À([0-9%]+).*¡æ\s*(.*)¦¸.*",
             name_expand_template='\\2',
             value_expand_template='\\2/\\1',
             reference='R',
             footprint='R_0805_2012Metric',
             symbol_pins=resistor_pins,
             symbol_rectangles=resistor_rectangles,
             text_posx=0.762,
             where_clause='"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "%805"')

# ===========================================================================================================================
# 1206 resistors
append_parts(lib_object=kicad_sym.KicadLibrary("build/jlcpcb-basic-resistor-1206.kicad_sym"),
             description_value_re="¡À([0-9%]+).*¡æ\s*(.*)¦¸.*",
             name_expand_template='\\2',
             value_expand_template='\\2/\\1',
             reference='R',
             footprint='R_1206_3216Metric',
             symbol_pins=resistor_pins,
             symbol_rectangles=resistor_rectangles,
             text_posx=0.762,
             where_clause='"First Category" = "Resistors" and "Second Category" = "Chip Resistor - Surface Mount" and "Package" like "1206"')

# ===========================================================================================================================
# All Capacitors
lib_capacitors_all = kicad_sym.KicadLibrary("build/jlcpcb-basic-capacitor.kicad_sym")
append_parts(lib_object=lib_capacitors_all,
             description_value_re="(.+)\s(.+)\s(.+)¡À.*",
             name_expand_template='0402_\\2_\\1_\\3',
             value_expand_template='\\2/\\1/\\3',
             reference='C',
             footprint='C_0402_1005Metric',
             symbol_pins=capacitor_pins,
             symbol_polylines=capacitor_polylines,
             text_posx=1.71,
             where_clause='"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%402"')
append_parts(lib_object=lib_capacitors_all,
             description_value_re="(.+)\s(.+)\s(.+)¡À.*",
             name_expand_template='0603_\\2_\\1_\\3',
             value_expand_template='\\2/\\1/\\3',
             reference='C',
             footprint='C_0603_1608Metric',
             symbol_pins=capacitor_pins,
             symbol_polylines=capacitor_polylines,
             text_posx=1.71,
             where_clause= '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%603"')
append_parts(lib_object=lib_capacitors_all,
             description_value_re="(.+)\s(.+)\s(.+)¡À.*",
             name_expand_template='0805_\\2_\\1_\\3',
             value_expand_template='\\2/\\1/\\3',
             reference='C',
             footprint='C_0805_2012Metric',
             symbol_pins=capacitor_pins,
             symbol_polylines=capacitor_polylines,
             text_posx=1.71,
             where_clause='"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%805"')
append_parts(lib_object=lib_capacitors_all,
             description_value_re="(.+)\s(.+)\s(.+)¡À.*",
             name_expand_template='1206_\\2_\\1_\\3',
             value_expand_template='\\2/\\1/\\3',
             reference='C',
             footprint='C_1206_3216Metric',
             symbol_pins=capacitor_pins,
             symbol_polylines=capacitor_polylines,
             text_posx=1.71,
             where_clause='"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "1206"')

# ===========================================================================================================================
# 0402 Capacitors
append_parts(lib_object=kicad_sym.KicadLibrary("build/jlcpcb-basic-capacitor-0402.kicad_sym"),
             description_value_re="(.+)\s(.+)\s(.+)¡À.*",
             name_expand_template='\\2_\\1_\\3',
             value_expand_template='\\2/\\1/\\3',
             reference='C',
             footprint='C_0402_1005Metric',
             symbol_pins=capacitor_pins,
             symbol_polylines=capacitor_polylines,
             text_posx=1.71,
             where_clause='"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%402"')
# ===========================================================================================================================
# 0603 Capacitors
append_parts(lib_object=kicad_sym.KicadLibrary("build/jlcpcb-basic-capacitor-0603.kicad_sym"),
             description_value_re="(.+)\s(.+)\s(.+)¡À.*",
             name_expand_template='\\2_\\1_\\3',
             value_expand_template='\\2/\\1/\\3',
             reference='C',
             footprint='C_0603_1608Metric',
             symbol_pins=capacitor_pins,
             symbol_polylines=capacitor_polylines,
             text_posx=1.71,
             where_clause= '"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%603"')
# ===========================================================================================================================
# 0805 Capacitors
append_parts(lib_object=kicad_sym.KicadLibrary("build/jlcpcb-basic-capacitor-0805.kicad_sym"),
             description_value_re="(.+)\s(.+)\s(.+)¡À.*",
             name_expand_template='\\2_\\1_\\3',
             value_expand_template='\\2/\\1/\\3',
             reference='C',
             footprint='C_0805_2012Metric',
             symbol_pins=capacitor_pins,
             symbol_polylines=capacitor_polylines,
             text_posx=1.71,
             where_clause='"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "%805"')
# ===========================================================================================================================
# 1206 Capacitors
append_parts(lib_object=kicad_sym.KicadLibrary("build/jlcpcb-basic-capacitor-1206.kicad_sym"),
             description_value_re="(.+)\s(.+)\s(.+)¡À.*",
             name_expand_template='\\2_\\1_\\3',
             value_expand_template='\\2/\\1/\\3',
             reference='C',
             footprint='C_1206_3216Metric',
             symbol_pins=capacitor_pins,
             symbol_polylines=capacitor_polylines,
             text_posx=1.71,
             where_clause='"First Category" = "Capacitors" and "Second Category" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT" and "Package" like "1206"')
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
