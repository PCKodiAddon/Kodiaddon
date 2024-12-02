import xbmcaddon
import xbmcgui

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

xbmcgui.Dialog().ok(addonname, "Hello from WeebayModz!")
