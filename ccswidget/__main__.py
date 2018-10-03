import os
import signal
import json
import subprocess
import random
import threading
import time

from urllib2 import Request, urlopen, URLError

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


APPINDICATOR_ID = 'CCS Updates'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('ccs.jpg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    t1 = threading.Thread(target=launch, args=())
    t1.start()
    gtk.main()

def build_menu():
    menu = gtk.Menu()

    item_site = gtk.MenuItem('Visit Site')
    item_site.connect('activate', open_site)
    menu.append(item_site)

    item_update = gtk.MenuItem('Update')
    item_update.connect('activate', update_now)
    menu.append(item_update)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    return menu

def open_site():
    webbrowser.open_new("http://www.google.com")

def fetch_update():
    return ("Nothing new")

def update_now(_):
    update_recieved = fetch_update()
    notify.Notification.new("<b>Update</b>", update_recieved, None).show()

def launch():
    last_update = ''
    while True:
        update_recieved = fetch_update()
        if update_recieved != last_update:
            notify.Notification.new("<b>Update</b>", update_recieved, None).show()
            last_update= update_recieved
        time.sleep(5)

def quit(_):
    notify.uninit()
    gtk.main_quit()

signal.signal(signal.SIGINT, signal.SIG_DFL)
main()
