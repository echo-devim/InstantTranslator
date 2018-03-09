#! /usr/bin/python

import sys
import os
import urllib
import requests
import json
import base64
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def getSelectedText():
    selectedText = os.popen('xclip -out -selection').read() #X11 Only

    if selectedText == "":
        print("No selected text in memory")
        sys.exit(0);

    return selectedText

def getTranslation(text): #en->it
    #baseUrl is encoded because it is an illegal call to the GT API (i.e. it is a workaround, authentication not required)
    #I would prefer to publish the url a little bit obfuscated
    baseUrl = base64.b64decode("aHR0cHM6Ly90cmFuc2xhdGUuZ29vZ2xlYXBpcy5jb20vdHJhbnNsYXRlX2Evc2luZ2xlP2NsaWVudD1ndHg=").decode('utf-8')
    #Source language (sl) could be also 'auto'
    response = requests.get(baseUrl + "&sl=en&tl=it&dt=t&q=" + urllib.parse.quote_plus(text)).content
    data = json.loads(response)
    return data[0][0][0]

def showWindow(text):
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    window.connect("leave-notify-event", Gtk.main_quit)
    window.set_position(Gtk.WindowPosition.MOUSE)
    label = Gtk.Label("<span font_desc='15.0'>" + text + "</span>")
    label.set_use_markup(True)
    #label.set_selectable(True)
    label.set_line_wrap(True)
    label.set_max_width_chars(50)
    label.set_margin_top(1)
    label.set_margin_bottom(1)
    window.add(label)
    window.set_decorated(False)
    window.set_keep_above(True)
    window.show_all()
    Gtk.main()

showWindow(getTranslation(getSelectedText()))
