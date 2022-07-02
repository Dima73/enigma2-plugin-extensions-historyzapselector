# -*- coding: utf-8 -*-
from . import _
from Screens.Screen import Screen
from Screens.EventView import EventViewSimple
from Screens.EpgSelection import EPGSelection
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap, NumberActionMap, HelpableActionMap
from Screens.HelpMenu import HelpableScreen
from Components.Sources.List import List
from Screens.ChoiceBox import ChoiceBox
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.config import config
from Tools.Directories import fileExists
from Tools.Alternatives import GetWithAlternative
from Screens.PictureInPicture import PictureInPicture
from Screens.ServiceInfo import ServiceInfo
import Screens.InfoBar
from Tools.BoundFunction import boundFunction
import Components.ParentalControl
from enigma import ePicLoad, eServiceReference, eServiceCenter, eEPGCache, iServiceInformation, eTimer, getDesktop
from ServiceReference import ServiceReference
try:
	from Components.Renderer.Picon import getPiconName
	getPiconsName = True
except:
	getPiconsName = False

FULLHD = False
if getDesktop(0).size().width() >= 1920:
	FULLHD = True


class PreviewZap(Screen):
	if FULLHD:
		skin = """<screen name="PreviewZap" flags="wfNoBorder" position="center,75" size="135,38" title="Preview" zPosition="-1">
			<eLabel text="Preview" position="0,0" size="135,38" foregroundColor="#00ff66" font="Regular;33" />
			</screen>"""
	else:
		skin = """<screen name="PreviewZap" flags="wfNoBorder" position="center,50" size="90,25" title="Preview" zPosition="-1">
				<eLabel text="Preview" position="0,0" size="90,25" foregroundColor="#00ff66" font="Regular;22" />
			</screen>"""


class FullEntryNumber(Screen):
	if FULLHD:
		skin = """<screen name="FullEntryNumber" position="center,center" size="1080,630" title=" " zPosition="-1">
			<widget name="text" font="Regular;26" position="8,15" size="338,600" zPosition="2" halign="left" backgroundColor="#31000000" transparent="1" />
			<widget name="text1" font="Regular;26" position="360,15" size="338,600" zPosition="2" halign="left" backgroundColor="#31000000" transparent="1" />
			<widget name="text2" font="Regular;26" position="713,15" size="338,600" zPosition="2" halign="left" backgroundColor="#31000000" transparent="1" />
		</screen>"""
	else:
		skin = """<screen name="FullEntryNumber" position="center,center" size="720,420" title=" " zPosition="-1">
			<widget name="text" font="Regular;17" position="5,10" size="225,400" zPosition="2" halign="left" backgroundColor="#31000000" transparent="1" />
			<widget name="text1" font="Regular;17" position="240,10" size="225,400" zPosition="2" halign="left" backgroundColor="#31000000" transparent="1" />
			<widget name="text2" font="Regular;17" position="475,10" size="225,400" zPosition="2" halign="left" backgroundColor="#31000000" transparent="1" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self['text'] = Label()
		self['text1'] = Label()
		self['text2'] = Label()
		self.setTitle(_("Use the number keys for zap to service"))

	def setInfo(self, entrylist=[]):
		text = text1 = text2 = ""
		i = 1
		for x in entrylist:
			if x[1] != "»":
				if i < 21:
					text += "%s) %s\n" % (x[1], x[2])
				elif 20 < i < 41:
					text1 += "%s) %s\n" % (x[1], x[2])
				elif 40 < i < 61:
					text2 += "%s) %s\n" % (x[1], x[2])
				i += 1
		self['text'].setText(text)
		self['text1'].setText(text1)
		self['text2'].setText(text2)

	def setTitleNumber(self, text=''):
		self.setTitle(text)


class HistoryZapSelector(Screen, HelpableScreen):
	searchPiconPaths = ['/usr/share/enigma2/picon/', '/media/hdd/picon/', '/media/usb/picon/']
	HistoryZapDefaultSkin = """
		<screen position="center,center" size="350,280" title="History zap...">
			<widget source="menu" render="Listbox" position="0,10" size="350,220" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (10, 2), size = (20, 20), font = 2, color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (40, 0), size = (290, 22), font = 1, flags = RT_HALIGN_LEFT, text = 2)
						],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17)],
					"itemHeight": 22
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="0,240" size="350,17" zPosition="5" font="Regular;13" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/little_buttons.png" position="0,240" size="350,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventSkin = """
		<screen position="center,center" size="600,280" title="History zap...">
			<widget source="menu" render="Listbox" position="0,10" size="600,220" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (0, 2), size = (20, 20), font = 2, color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (30, 0), size = (260, 22), font = 1, flags = RT_HALIGN_LEFT, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (300, 2), size = (300, 19), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000)
						],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17)],
					"itemHeight": 22
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,240" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="0,240" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventPiconSkin = """
		<screen position="center,center" size="620,300" title="History zap...">
			<widget source="menu" render="Listbox" position="0,0" size="620,256" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (57, 5), size = (20, 20), font = 2,  color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (80, 4), size = (260, 22), font = 1, flags = RT_HALIGN_LEFT, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (350, 6), size = (270, 19), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryPixmapAlphaBlend(pos=(0, 0), size=(50, 30), png=6)
						],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17)],
					"itemHeight": 32
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,260" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="10,260" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventDurationSkin = """
		<screen position="center,center" size="600,340" title="History zap...">
			<widget source="menu" render="Listbox" position="0,0" size="600,295" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (0, 10), size = (20, 20), font = 2, color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (30, 0), size = (260, 21), font = 1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (300, 10), size = (300, 22), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (30, 24), size = (260, 17), font = 2, flags = RT_HALIGN_LEFT, text = 5, color = 0x00999999, color_sel = 0x00999999)
						],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17)],
					"itemHeight": 42
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,300" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="0,300" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventDurationBarSkin = """
		<screen position="center,center" size="600,340" title="History zap...">
			<widget source="menu" render="Listbox" position="0,0" size="600,295" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (0, 10), size = (20, 20), font = 2, color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (30, 0), size = (260, 21), font = 1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (300, 10), size = (300, 22), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryProgress(pos = (30, 24), size = (120, 12), percent = -5, borderWidth = 1, foreColor = 0x0056c856, foreColorSelected = 0x0058bcff),
							MultiContentEntryText(pos = (160, 22), size = (50, 17), font = 3, flags = RT_HALIGN_LEFT, text = 7, color = 0x00999999, color_sel = 0x009999ff)
						],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17), gFont("Regular", 16)],
					"itemHeight": 42
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,300" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="0,300" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventDurationPiconSkin = """
		<screen position="center,center" size="620,340" title="History zap...">
			<widget source="menu" render="Listbox" position="0,0" size="620,295" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (57, 10), size = (20, 20), font = 2, color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (80, 0), size = (260, 21), font = 1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (350, 10), size = (270, 22), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (80, 24), size = (260, 17), font = 2, flags = RT_HALIGN_LEFT, text = 5, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryPixmapAlphaBlend(pos=(0, 6), size=(50, 30), png=6)
						],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17)],
					"itemHeight": 42
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,300" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="10,300" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventDurationPiconBarSkin = """
		<screen position="center,center" size="620,340" title="History zap...">
			<widget source="menu" render="Listbox" position="0,0" size="620,295" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (57, 10), size = (20, 20), font = 2, color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (80, 0), size = (260, 21), font = 1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (350, 10), size = (270, 22), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryProgress(pos = (80, 24), size = (120, 12), percent = -5, borderWidth = 1, foreColor = 0x0056c856, foreColorSelected = 0x0058bcff),
							MultiContentEntryText(pos = (210, 22), size = (50, 17), font = 3, flags = RT_HALIGN_LEFT, text = 7, color = 0x00999999, color_sel = 0x009999ff),
							MultiContentEntryPixmapAlphaBlend(pos=(0, 6), size=(50, 30), png=6)
						],
					 "fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17), gFont("Regular", 16)],
					 "itemHeight": 42
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,300" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="10,300" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionSkin = """
		<screen position="center,center" size="620,340" title="History zap...">
			<widget source="menu" render="Listbox" position="0,0" size="620,295" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (0, 10), size = (20, 20), font = 2, color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (30, 0), size = (260, 21), font = 1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (300, 5), size = (320, 20), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (30, 24), size = (590, 17), font = 2, flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999)
						],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17)],
					"itemHeight": 42
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,300" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="10,300" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionDurationSkin = """
		<screen position="center,center" size="620,340" title="History zap...">
			<widget source="menu" render="Listbox" position="0,0" size="620,295" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (0, 10), size = (20, 20), font = 2, color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (30, 0), size = (260, 21), font = 1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (300, 5), size = (320, 20), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (30, 24), size = (180, 17), font = 3, flags = RT_HALIGN_LEFT, text = 5, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryText(pos = (230, 25), size = (390, 17), font = 3, flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999)
						],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17), gFont("Regular", 16)],
					"itemHeight": 42
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,300" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="10,300" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionDurationBarSkin = """
		<screen position="center,center" size="620,340" title="History zap...">
			<widget source="menu" render="Listbox" position="0,0" size="620,295" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (0, 10), size = (20, 20), font = 2, color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (30, 0), size = (260, 21), font = 1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (300, 5), size = (320, 20), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryProgress(pos = (30, 24), size = (120, 12), percent = -5, borderWidth = 1, foreColor = 0x0056c856, foreColorSelected = 0x0058bcff),
							MultiContentEntryText(pos = (160, 22), size = (50, 17), font = 3, flags = RT_HALIGN_LEFT, text = 7, color = 0x00999999, color_sel = 0x009999ff),
						MultiContentEntryText(pos = (230, 25), size = (390, 17), font = 3, flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999)
					],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17), gFont("Regular", 16)],
					"itemHeightt": 42
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,300" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="10,300" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionPiconSkin = """
		<screen position="center,center" size="620,340" title="History zap...">
			<widget source="menu" render="Listbox" position="0,0" size="620,295" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (57, 10), size = (20, 20), font = 2, color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (80, 0), size = (260, 21), font = 1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (350, 5), size = (270, 22), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (80, 24), size = (540, 17), font = 2, flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryPixmapAlphaBlend(pos=(0, 6), size=(50, 30), png=6)
						],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17)],
					"itemHeight": 42
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,300" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="10,300" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionDurationPiconSkin = """
		<screen position="center,center" size="620,340" title="History zap...">
			<widget source="menu" render="Listbox" position="0,0" size="620,295" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (57, 10), size = (20, 20), font = 2, color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (80, 0), size = (260, 21), font = 1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (350, 5), size = (270, 22), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (80, 25), size = (180, 17), font = 3, flags = RT_HALIGN_LEFT, text = 5, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryText(pos = (270, 25), size = (350, 17), font = 3, flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryPixmapAlphaBlend(pos=(0, 6), size=(50, 30), png=6)
						],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17), gFont("Regular", 16)],
					"itemHeight": 42
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,300" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="10,300" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionDurationBarPiconSkin = """
		<screen position="center,center" size="620,340" title="History zap...">
			<widget source="menu" render="Listbox" position="0,0" size="620,295" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (57, 10), size = (20, 20), font = 2, color =0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (80, 0), size = (260, 21), font = 1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (350, 5), size = (270, 22), font = 2, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryProgress(pos = (80, 25), size = (120, 12), percent = -5, borderWidth = 1, foreColor = 0x0056c856, foreColorSelected = 0x0058bcff),
							MultiContentEntryText(pos = (210, 23), size = (50, 17), font = 3, flags = RT_HALIGN_LEFT, text = 7, color = 0x00999999, color_sel = 0x009999ff),
							MultiContentEntryText(pos = (270, 25), size = (350, 17), font = 3, flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryPixmapAlphaBlend(pos=(0, 6), size=(50, 30), png=6)
						],
					"fonts": [gFont("Regular", 22), gFont("Regular", 20), gFont("Regular", 17), gFont("Regular", 16)],
					"itemHeight": 42
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="80,300" size="500,18" zPosition="5" font="Regular;16" transparent="1" />
			<widget name="menu_buttons" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons.png" position="10,300" size="600,40" zPosition="4" transparent="1"/>
		</screen>"""

	HistoryZapDefaultSkinFullHD = """
		<screen position="center,center" size="675,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="675,822" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (15, 3), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (68, 3), size = (578, 39), flags = RT_HALIGN_LEFT, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 48
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="120,855" size="525,22" zPosition="5" font="Regular;19" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/little_buttons_fhd.png" position="72,885" size="555,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,822" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (15, 3), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (68, 3), size = (390, 39), flags = RT_HALIGN_LEFT, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (473, 3), size = (705, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 48
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="285,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="150,855" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventPiconSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,832" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (80, 21), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (128, 3), size = (1043, 39), flags = RT_HALIGN_LEFT, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (128, 45), size = (1043, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryPixmapAlphaBlend(pos=(1, 19), size=(75, 45), png=6)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 92
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="285,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="150,885" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventDurationSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,832" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (15, 21), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (68, 3), size = (390, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (473, 3), size = (698, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (68, 45), size = (390, 39), flags = RT_HALIGN_LEFT, text = 5, color = 0x00999999, color_sel = 0x00999999)
						],
					 "fonts": [gFont("Regular", 33), ],
					 "itemHeight": 92
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="285,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="150,885" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventDurationBarSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,832" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (15, 21), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (68, 3), size = (390, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (473, 3), size = (698, 39),flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryProgress(pos = (68, 57), size = (278, 18), percent = -5, borderWidth = 1, foreColor = 0x0056c856, foreColorSelected = 0x0058bcff),
							MultiContentEntryText(pos = (368, 45), size = (68, 39), flags = RT_HALIGN_LEFT, text = 7, color = 0x00999999, color_sel = 0x009999ff)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 92
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="285,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="150,885" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventDurationPiconSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,832" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (80, 21), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (128, 3), size = (390, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (533, 3), size = (638, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (128, 51), size = (390, 39), flags = RT_HALIGN_LEFT, text = 5, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryPixmapAlphaBlend(pos=(1, 19), size=(75, 45), png=6)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 92
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="285,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="150,885" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapEventDurationPiconBarSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,832" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (80, 21), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (128, 3), size = (390, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (533, 3), size = (638, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryProgress(pos = (128, 57), size = (278, 18), percent = -5, borderWidth = 1, foreColor = 0x0056c856, foreColorSelected = 0x0058bcff),
							MultiContentEntryText(pos = (435, 39), size = (68, 39), flags = RT_HALIGN_LEFT, text = 7, color = 0x00999999, color_sel = 0x009999ff),
							MultiContentEntryPixmapAlphaBlend(pos=(1, 19), size=(75, 45), png=6)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 92
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="120,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="15,885" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,832" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (15, 21), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (68, 3), size = (390, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (473, 3), size = (698, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (68, 45), size = (1103, 39), flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 92
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="285,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="150,885" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionDurationSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,832" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (15, 21), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (68, 3), size = (390, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (473, 3), size = (698, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (68, 45), size = (390, 39), flags = RT_HALIGN_LEFT, text = 5, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryText(pos = (473, 45), size = (698, 39), flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 92
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="285,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="150,885" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionDurationBarSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,832" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (15, 21), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (68, 3), size = (390, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (473, 3), size = (698, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryProgress(pos = (68, 57), size = (278, 18), percent = -5, borderWidth = 1, foreColor = 0x0056c856, foreColorSelected = 0x0058bcff),
							MultiContentEntryText(pos = (368, 45), size = (68, 39), flags = RT_HALIGN_LEFT, text = 7, color = 0x00999999, color_sel = 0x009999ff),
							MultiContentEntryText(pos = (473, 45), size = (698, 39), flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 92
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="285,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="150,885" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionPiconSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,832" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (80, 21), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (128, 3), size = (390, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (533, 3), size = (638, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (128, 45), size = (1043, 39), flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryPixmapAlphaBlend(pos=(1, 19), size=(75, 45), png=6)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 92
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="285,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="150,885" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionDurationPiconSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,832" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (80, 21), size = (39, 39), color = 0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (128, 3), size = (390, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (533, 3), size = (638, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryText(pos = (128, 45), size = (390, 39), flags = RT_HALIGN_LEFT, text = 5, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryText(pos = (533, 45), size = (638, 39), flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryPixmapAlphaBlend(pos=(1, 19), size=(75, 45), png=6)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 92
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="285,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="150,885" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""
	HistoryZapDescriptionDurationBarPiconSkinFullHD = """
		<screen position="center,center" size="1200,960" title="History zap...">
			<widget source="menu" render="Listbox" position="0,8" size="1200,832" scrollbarMode="showNever">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (80, 21), size = (39, 39), color =0x00ffc000, color_sel = 0x00ffc000, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 1),
							MultiContentEntryText(pos = (128, 3), size = (390, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_TOP, text = 2, color = 0x00ffffff, color_sel = 0x00ffffff),
							MultiContentEntryText(pos = (533, 3), size = (638, 39), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3, color = 0x00ffc000, color_sel = 0x00ffc000),
							MultiContentEntryProgress(pos = (128, 57), size = (278, 18), percent = -5, borderWidth = 1, foreColor = 0x0056c856, foreColorSelected = 0x0058bcff),
							MultiContentEntryText(pos = (435, 45), size = (68, 39), flags = RT_HALIGN_LEFT, text = 7, color = 0x00999999, color_sel = 0x009999ff),
							MultiContentEntryText(pos = (533, 45), size = (638, 39), flags = RT_HALIGN_LEFT, text = 4, color = 0x00999999, color_sel = 0x00999999),
							MultiContentEntryPixmapAlphaBlend(pos=(1, 19), size=(75, 45), png=6)
						],
					 "fonts": [gFont("Regular", 33)],
					 "itemHeight": 92
					}
				</convert>
			</widget>
			<widget name="text_buttons" position="285,855" size="750,23" zPosition="5" font="Regular;20" transparent="1" />
			<widget name="menu_buttons" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/buttons_fhd.png" position="150,885" size="900,60" zPosition="4" transparent="1"/>
		</screen>"""

	def __init__(self, session, items=[], sel_item=0, mark_item=0, invert_items=False, redirect_buttons=False, wrap_around=True):
		Screen.__init__(self, session)
		if FULLHD:
			self.entry = 7
			if config.plugins.SetupZapSelector.event.value == "0":
					self.skin = self.HistoryZapDefaultSkinFullHD
					self.entry = 10
					self.skinName = "HistoryZapDefaultSkinFullHD"
			elif config.plugins.SetupZapSelector.event.value == "1":
				if not config.plugins.SetupZapSelector.duration.value and not config.plugins.SetupZapSelector.picon.value:
					self.skin = self.HistoryZapEventSkinFullHD
					self.skinName = "HistoryZapEventSkinFullHD"
					self.entry = 10
				if not config.plugins.SetupZapSelector.duration.value and config.plugins.SetupZapSelector.picon.value:
					self.skin = self.HistoryZapEventPiconSkinFullHD
					self.skinName = "HistoryZapEventPiconSkinFullHD"
					self.entry = 8
				if config.plugins.SetupZapSelector.duration.value and not config.plugins.SetupZapSelector.picon.value:
					if config.plugins.SetupZapSelector.duration_type.value == "1":
						self.skin = self.HistoryZapEventDurationBarSkinFullHD
						self.skinName = "HistoryZapEventDurationBarSkinFullHD"
					else:
						self.skin = self.HistoryZapEventDurationSkinFullHD
						self.skinName = "HistoryZapEventDurationSkinFullHD"
				if config.plugins.SetupZapSelector.duration.value and config.plugins.SetupZapSelector.picon.value:
					if config.plugins.SetupZapSelector.duration_type.value == "1":
						self.skin = self.HistoryZapEventDurationPiconBarSkinFullHD
						self.skinName = "HistoryZapEventDurationPiconBarSkinFullHD"
					else:
						self.skin = self.HistoryZapEventDurationPiconSkinFullHD
						self.skinName = "HistoryZapEventDurationPiconSkinFullHD"
			else:
				if not config.plugins.SetupZapSelector.duration.value and not config.plugins.SetupZapSelector.picon.value:
					self.skin = self.HistoryZapDescriptionSkinFullHD
					self.skinName = "HistoryZapDescriptionSkinFullHD"
				if not config.plugins.SetupZapSelector.duration.value and config.plugins.SetupZapSelector.picon.value:
					self.skin = self.HistoryZapDescriptionPiconSkinFullHD
					self.skinName = "HistoryZapDescriptionPiconSkinFullHD"
				if config.plugins.SetupZapSelector.duration.value and not config.plugins.SetupZapSelector.picon.value:
					if config.plugins.SetupZapSelector.duration_type.value == "1":
						self.skin = self.HistoryZapDescriptionDurationBarSkinFullHD
						self.skinName = "HistoryZapDescriptionDurationBarSkinFullHD"
					else:
						self.skin = self.HistoryZapDescriptionDurationSkinFullHD
						self.skinName = "HistoryZapDescriptionDurationSkinFullHD"
				if config.plugins.SetupZapSelector.duration.value and config.plugins.SetupZapSelector.picon.value:
					if config.plugins.SetupZapSelector.duration_type.value == "1":
						self.skin = self.HistoryZapDescriptionDurationBarPiconSkinFullHD
						self.skinName = "HistoryZapDescriptionDurationBarPiconSkinFullHD"
					else:
						self.skin = self.HistoryZapDescriptionDurationPiconSkinFullHD
						self.skinName = "HistoryZapDescriptionDurationPiconSkinFullHD"
		else:
			self.entry = 7
			if config.plugins.SetupZapSelector.event.value == "0":
					self.skin = self.HistoryZapDefaultSkin
					self.entry = 10
					self.skinName = "HistoryZapDefaultSkin"
			elif config.plugins.SetupZapSelector.event.value == "1":
				if not config.plugins.SetupZapSelector.duration.value and not config.plugins.SetupZapSelector.picon.value:
					self.skin = self.HistoryZapEventSkin
					self.skinName = "HistoryZapEventSkin"
					self.entry = 10
				if not config.plugins.SetupZapSelector.duration.value and config.plugins.SetupZapSelector.picon.value:
					self.skin = self.HistoryZapEventPiconSkin
					self.skinName = "HistoryZapEventPiconSkin"
					self.entry = 8
				if config.plugins.SetupZapSelector.duration.value and not config.plugins.SetupZapSelector.picon.value:
					if config.plugins.SetupZapSelector.duration_type.value == "1":
						self.skin = self.HistoryZapEventDurationBarSkin
						self.skinName = "HistoryZapEventDurationBarSkin"
					else:
						self.skin = self.HistoryZapEventDurationSkin
						self.skinName = "HistoryZapEventDurationSkin"
				if config.plugins.SetupZapSelector.duration.value and config.plugins.SetupZapSelector.picon.value:
					if config.plugins.SetupZapSelector.duration_type.value == "1":
						self.skin = self.HistoryZapEventDurationPiconBarSkin
						self.skinName = "HistoryZapEventDurationPiconBarSkin"
					else:
						self.skin = self.HistoryZapEventDurationPiconSkin
						self.skinName = "HistoryZapEventDurationPiconSkin"
			else:
				if not config.plugins.SetupZapSelector.duration.value and not config.plugins.SetupZapSelector.picon.value:
					self.skin = self.HistoryZapDescriptionSkin
					self.skinName = "HistoryZapDescriptionSkin"
				if not config.plugins.SetupZapSelector.duration.value and config.plugins.SetupZapSelector.picon.value:
					self.skin = self.HistoryZapDescriptionPiconSkin
					self.skinName = "HistoryZapDescriptionPiconSkin"
				if config.plugins.SetupZapSelector.duration.value and not config.plugins.SetupZapSelector.picon.value:
					if config.plugins.SetupZapSelector.duration_type.value == "1":
						self.skin = self.HistoryZapDescriptionDurationBarSkin
						self.skinName = "HistoryZapDescriptionDurationBarSkin"
					else:
						self.skin = self.HistoryZapDescriptionDurationSkin
						self.skinName = "HistoryZapDescriptionDurationSkin"
				if config.plugins.SetupZapSelector.duration.value and config.plugins.SetupZapSelector.picon.value:
					if config.plugins.SetupZapSelector.duration_type.value == "1":
						self.skin = self.HistoryZapDescriptionDurationBarPiconSkin
						self.skinName = "HistoryZapDescriptionDurationBarPiconSkin"
					else:
						self.skin = self.HistoryZapDescriptionDurationPiconSkin
						self.skinName = "HistoryZapDescriptionDurationPiconSkin"

		HelpableScreen.__init__(self)
		self.session = session
		self["menu_buttons"] = Pixmap()
		self.InfoBarInstance = Screens.InfoBar.InfoBar.instance
		config.plugins.SetupZapSelector.preview.value = False
		self.number_zap = config.plugins.SetupZapSelector.number_zap.value
		self.redirectButton = redirect_buttons
		self.invertItems = invert_items
		if self.invertItems:
			self.currentPos = len(items) - sel_item - 1
		else:
			self.currentPos = sel_item
		self["actions"] = HelpableActionMap(self, "HistoryZapActions",
			{
				"ok": (self.okbuttonClick, _("zap to service")),
				"cancel": (self.cancelClick, _("exit")),
				"jumpPreviousMark": (self.prev, _("previous entry")),
				"jumpNextMark": (self.nextEntry, _("next entry")),
				"toggleMark": (self.okbuttonClick, _("zap to service")),
				"showInfo": (self.epgmapbuttonClick, _("open single EPG")),
				"showGuide": (self.infomapbuttonClick, _("open Event View")),
				"showGuideLong": (self.epgmapbuttonClick, _("open single EPG")),
				"showInfoLong": (self.infomapbuttonClick, _("open Event View")),
				"menu": (self.menubuttonClick, _("open list options")),
				"red": (self.deleteCurrentEntryClick, _("delete selected entry")),
				"green": (self.greenbuttonClick, _("clear history list")),
				"yellow": (self.yellowbuttonClick, _("show all list")),
				"blue": (self.bluebuttonClick, _("preview for selected entry")),
				"showServiceInfo": (self.audiobuttonClick, _("Show transponder info")),
				}, -1
		)
		if self.number_zap:
			self["Numberactions"] = NumberActionMap(["SetupActions", "ShortcutActions"],
				{
					"cancel": self.quit,
					"ok": self.keyOK,
					"1": self.keyNumberGlobal,
					"2": self.keyNumberGlobal,
					"3": self.keyNumberGlobal,
					"4": self.keyNumberGlobal,
					"5": self.keyNumberGlobal,
					"6": self.keyNumberGlobal,
					"7": self.keyNumberGlobal,
					"8": self.keyNumberGlobal,
					"9": self.keyNumberGlobal,
					"0": self.keyNumberGlobal
				}, prio=-1)
		self.numTimer = eTimer()
		self.numTimer.callback.append(self.keyOK)
		self.numberString = None
		self.service_ref = None
		self.picon = ePicLoad()
		self.epglist = None
		self.list = []
		cnt = 0
		for x in items:
			marker = ""
			if self.number_zap:
				marker = "%d" % (len(items) - cnt - 1)
			perc = ""
			if config.plugins.SetupZapSelector.duration_type.value == "1":
				if x[4] != -1:
					perc = str(x[4]) + '%'
			png = ""
			if config.plugins.SetupZapSelector.picon.value:
				if getPiconsName:
					picon = getPiconName(str(ServiceReference(x[1])))
				else:
					picon = self.findPicon(str(ServiceReference(x[1])))
				if picon != "":
					psw = 50
					psh = 30
					if FULLHD:
						psw = 75
						psh = 45
					self.picon.setPara((psw, psh, 1, 1, False, 1, '#000f0f0f'))
					self.picon.startDecode(picon, 0, 0, False)
					png = self.picon.getData()
			if self.invertItems:
				self.list.insert(0, (x[1], cnt == mark_item and "»" or marker, x[0], x[2], x[3], x[4], png, perc))
			else:
				self.list.append((x[1], cnt == mark_item and "»" or marker, x[0], x[2], x[3], x[4], png, perc))
			cnt += 1
		self["menu"] = List(self.list, enableWrapAround=wrap_around)
		if not config.plugins.SetupZapSelector.show_button.value:
			self["menu_buttons"].hide()
			self['text_buttons'] = Label()
		else:
			if len(self.list) < 2:
				self['text_buttons'] = Label()
			else:
				if config.plugins.SetupZapSelector.event.value == "0":
					if self.number_zap and len(self.list) > self.entry:
						self['text_buttons'] = Label(_("Del entry  Clear history  List  Preview"))
					else:
						self['text_buttons'] = Label(_("Del entry  Clear history        Preview"))
				else:
					if self.number_zap and len(self.list) > self.entry:
						self['text_buttons'] = Label(_("Delete selected  Clear history  All list       Preview"))
					else:
						self['text_buttons'] = Label(_("Delete selected  Clear history                 Preview"))
		self.firstShown = False
		self.previewActive = None
		self.preview_zap = False
		self.numberZapActive = False
		self.FullEntryNumber = None
		self.FullEntryActive = False
		self.onShown.append(self.__onShown)
		self.setup_title = _("History zap: count %d") % len(items)
		self.setTitle(self.setup_title)
		try:
			self.playservice = self.session.nav.getCurrentlyPlayingServiceOrGroup()
		except:
			self.playservice = self.session.nav.getCurrentlyPlayingServiceReference()
		service = len(self.list) > 0 and self.list[0][0] or None
		if self.playservice is None or (service and service != self.playservice):
			self.playservice = service

	def __onShown(self):
		if not self.firstShown:
			self["menu"].index = self.currentPos
			self.firstShown = True

	def prev(self):
		if self.redirectButton:
			self.down()
		else:
			self.up()

	def nextEntry(self):
		if self.redirectButton:
			self.up()
		else:
			self.down()

	def up(self):
		self["menu"].selectPrevious()

	def down(self):
		self["menu"].selectNext()

	def getCurrent(self):
		cur = self["menu"].current
		return cur and cur[0]

	def keyNumberGlobal(self, number):
		if self.preview_zap:
			return
		if len(self.list) <= 1:
			if number == 0:
				return 0
			return
		self.numTimer.stop()
		self.service_ref = None
		if self.numberString is None:
			if number == 0:
				return 0
			self.numberString = str(number)
			self.numberZapActive = True
			self.numTimer.start(2500, True)
		else:
			self.numberString = self.numberString + str(number)
			self.numberZapActive = True
			self.numTimer.start(1000, True)
		self.service_ref, service_name = self.searchNumber(int(self.numberString))
		if self.service_ref is not None:
			new_title = _("%s  number: %s") % (service_name, self.numberString)
		else:
			new_title = _("Invalid number: %s") % self.numberString
		if self.FullEntryNumber is not None:
			self.FullEntryNumber.setTitleNumber(text=new_title)
		self.setTitle(new_title)
		if len(self.numberString) >= 3:
			self.keyOK()

	def searchNumber(self, number):
		for x in self.list:
			if x[1] not in ("»", "") and int(x[1]) == number:
				return x[0], x[2]
		return None, ''

	def keyOK(self):
		if self.numberZapActive:
			self.numberZapActive = False
			self.numberString = None
			self.numTimer.stop()
			if self.service_ref is not None:
				self.close(self.service_ref)
			else:
				new_title = _("History zap: count %d") % len(self.list)
				self.setTitle(new_title)
				if self.FullEntryNumber is not None:
					self.FullEntryNumber.setTitleNumber(text='')
		else:
			return 0

	def quit(self):
		if self.numberZapActive:
			self.numberZapActive = False
			self.numberString = None
			self.numTimer.stop()
			new_title = _("History zap: count %d") % len(self.list)
			self.setTitle(new_title)
			if self.FullEntryNumber is not None:
				self.FullEntryNumber.setTitleNumber(text='')
		else:
			return 0

	def yellowbuttonClick(self):
		if self.preview_zap or self.numberZapActive:
			return
		if self.FullEntryActive:
			if self.FullEntryNumber is not None:
				self.FullEntryNumber.hide()
				self.show()
				self.FullEntryActive = False
				return
		if self.number_zap and len(self.list) > self.entry:
			try:
				if self.FullEntryNumber is None:
					self.FullEntryNumber = self.session.instantiateDialog(FullEntryNumber)
					if self.FullEntryNumber is not None:
						self.FullEntryNumber.show()
						self.FullEntryNumber.setInfo(entrylist=self.list)
				else:
					self.FullEntryNumber.show()
					self.FullEntryNumber.setInfo(entrylist=self.list)
				self.FullEntryActive = True
				self.hide()
			except:
				self.FullEntryNumber = None

	def okbuttonClick(self):
		if self.FullEntryActive:
			if self.FullEntryNumber is not None:
				self.FullEntryNumber.hide()
				self.show()
				self.FullEntryActive = False
				return
		if self.preview_zap:
			self.preview_zap = False
			new_title = _("History zap: count %d") % len(self.list)
			self.setTitle(new_title)
			self.closePreviewActive()
			self.show()
		else:
			pip_config = config.plugins.SetupZapSelector.pip_zap.value
			isPip = hasattr(self.session, 'pipshown') and self.session.pipshown
			if isPip and pip_config != "0":
				doPip = self.InfoBarInstance and self.InfoBarInstance.servicelist and hasattr(self.InfoBarInstance.servicelist, 'dopipzap') and self.InfoBarInstance.servicelist.dopipzap
				if self.InfoBarInstance:
					if pip_config == "1":
						text = _("Zap as:")
						cur_ref = self.getCurrent()
						if cur_ref and self.playservice and self.playservice != cur_ref:
							menu = [(_("Main screen"), "main"), (_("Standard PiP"), "standard"), (_("Pipzap"), "pipzap")]
						else:
							menu = [(_("Standard PiP"), "standard"), (_("Pipzap"), "pipzap")]

						def extraAction(choice):
							if choice:
								if choice[1] == "main":
									self.close(self.getCurrent())
								elif choice[1] == "standard":
									self.setPipZap(type="3", dopipzap=doPip, ispip=isPip)
								elif choice[1] == "pipzap":
									self.setPipZap(type="2", dopipzap=doPip, ispip=isPip)
						self.session.openWithCallback(extraAction, ChoiceBox, title=text, list=menu)
					elif pip_config == "4":
						self.setPipZap(type="4", dopipzap=doPip, ispip=isPip)
					elif doPip and pip_config == "2":
						self.setPipZap(type="2", dopipzap=doPip, ispip=isPip)
					elif not doPip and pip_config == "3":
						self.setPipZap(type="3", dopipzap=doPip, ispip=isPip)
					else:
						self.close(self.getCurrent())
				else:
					self.close(self.getCurrent())
			else:
				self.close(self.getCurrent())

	def setPipZap(self, type="0", dopipzap=False, ispip=False, checkParentalControl=True, ref=None):
		if type != "0" and self.InfoBarInstance.servicelist:
			nref = ref or self.getCurrent()
			start = False
			try:
				playservice = self.session.nav.getCurrentlyPlayingServiceOrGroup()
			except:
				playservice = self.session.nav.getCurrentlyPlayingServiceReference()
			if nref:
				if (not playservice or playservice != nref):
					if (not checkParentalControl or Components.ParentalControl.parentalControl.isServicePlayable(nref, boundFunction(self.setPipZap, type=type, dopipzap=dopipzap, ispip=ispip, checkParentalControl=False))):
						start = True
				else:
					start = True
				if start:
					if ispip:
						if dopipzap:
							self.InfoBarInstance.servicelist.togglePipzap()
						if hasattr(self.session, 'pip'):
							del self.session.pip
						self.session.pipshown = False
					self.session.pip = self.session.instantiateDialog(PictureInPicture)
					self.session.pip.show()
					if self.session.pip.playService(nref):
						self.session.pipshown = True
						self.session.pip.servicePath = self.InfoBarInstance.servicelist.getCurrentServicePath()
						hlen = len(self.InfoBarInstance.servicelist.history)
						pos = 0
						for x in self.InfoBarInstance.servicelist.history:
							if x[-1] == nref:
								break
							pos += 1
						if pos < hlen:
							if dopipzap and type != "3" or type == "2":
								self.InfoBarInstance.servicelist.clearPath()
								self.InfoBarInstance.servicelist.recallBouquetMode()
								if self.InfoBarInstance.servicelist.bouquet_root:
									self.InfoBarInstance.servicelist.enterPath(self.InfoBarInstance.servicelist.bouquet_root)
								self.InfoBarInstance.servicelist.enterPath(len(x) > 2 and x[1] or x[0])
								self.InfoBarInstance.servicelist.saveRoot()
								self.InfoBarInstance.servicelist.togglePipzap()
								self.InfoBarInstance.servicelist.startRoot = None
								self.InfoBarInstance.servicelist.rootChanged = False
								self.InfoBarInstance.servicelist.revertMode = None
								self.session.pip.servicePath = self.InfoBarInstance.servicelist.getCurrentServicePath()
						self.close(None)
					else:
						self.session.pipshown = False
						del self.session.pip
						self.session.openWithCallback(boundFunction(self.close, None), MessageBox, _("Could not open Picture in Picture"), MessageBox.TYPE_ERROR)
				else:
					self.close(None)
			else:
				self.close(None)
		else:
			self.close(None)

	try:
		def zapToClick(self, ref=None, preview=False, zapback=False):
			if ref is not None and not preview and not zapback:
				self.closePreviewActive()
				self.close(self.getCurrent())
	except:
		pass

	def epgbuttonClick(self):
		cur = self["menu"].current
		if cur and cur[0]:
			serviceHandler = eServiceCenter.getInstance()
			info = serviceHandler.info(cur[0])
			event = info and info.getEvent(cur[0])
			if event:
				try:
					self.session.open(EPGSelection, cur[0], zapFunc=self.zapToClick)
				except:
					pass

	def audiobuttonClick(self):
		cur = self["menu"].current
		try:
			if cur and cur[0] and cur[0].valid():
				current = cur[0]
				if current.flags & eServiceReference.isGroup:
					playingref = self.session.nav.getCurrentlyPlayingServiceOrGroup()
					if playingref and playingref == current:
						current = self.session.nav.getCurrentlyPlayingServiceReference()
					else:
						current = eServiceReference(GetWithAlternative(current.toString()))
				self.session.open(ServiceInfo, current)
		except:
			pass

	def infomapbuttonClick(self):
		if self.preview_zap or self.numberZapActive or self.FullEntryActive:
			return
		if config.plugins.SetupZapSelector.map_key.value:
			self.epgbuttonClick()
		else:
			self.infobuttonClick()

	def epgmapbuttonClick(self):
		if self.preview_zap or self.numberZapActive or self.FullEntryActive:
			return
		if not config.plugins.SetupZapSelector.map_key.value:
			self.epgbuttonClick()
		else:
			self.infobuttonClick()

	def infobuttonClick(self):
		epglist = []
		self.epglist = epglist
		cur = self["menu"].current
		if cur and cur[0]:
			serviceHandler = eServiceCenter.getInstance()
			info = serviceHandler.info(cur[0])
			event = info and info.getEvent(cur[0])
			if event:
				epglist.append(event)
			try:
				epg = eEPGCache.getInstance()
				next_event = epg.lookupEventTime(cur[0], -1, 1)
				if next_event:
					epglist.append(next_event)
			except:
				pass
			if event:
				self.session.open(EventViewSimple, event, ServiceReference(cur[0]), self.eventViewCallback, self.openSimilarList)

	def eventViewCallback(self, setEvent, setService, val):
		epglist = self.epglist
		if epglist is None:
			return
		if len(epglist) > 1:
			tmp = epglist[0]
			epglist[0] = epglist[1]
			epglist[1] = tmp
			setEvent(epglist[0])

	def openSimilarList(self, eventid, refstr):
		self.session.open(EPGSelection, refstr, None, eventid)

	def closePreviewActive(self):
		if self.previewActive is not None:
				try:
					self.previewActive.hide()
					self.previewActive = None
				except:
					self.previewActive = None

	def cancelClick(self):
		if self.FullEntryActive:
			if self.FullEntryNumber is not None:
				self.FullEntryNumber.hide()
				self.show()
				self.FullEntryActive = False
				return
		self.closePreviewActive()
		if config.plugins.SetupZapSelector.preview.value:
			self.close(self.playservice)
		else:
			self.close(None)

	def bluebuttonClick(self):
		if self.preview_zap or self.numberZapActive or self.FullEntryActive:
			return
		cur_ref = self.getCurrent()
		if cur_ref and self.playservice and self.playservice != cur_ref:
			if config.plugins.SetupZapSelector.warning_message.value:
				self.session.openWithCallback(self.answerZap, MessageBox, _("Preview zap to service ?"), type=MessageBox.TYPE_YESNO)
			else:
				self.answerZap(True)

	def answerZap(self, ret):
		if ret:
			cur = self["menu"].current
			cur_ref = cur and cur[0]
			if cur_ref and self.playservice and self.playservice != cur_ref:
				self.session.nav.playService(cur_ref, adjust=False)
				self.preview_zap = True
				config.plugins.SetupZapSelector.preview.value = True
				name = cur[2]
				if name != "":
					new_title = _("%s") % name
					self.setTitle(new_title)
				try:
					if self.previewActive is None:
						self.previewActive = self.session.instantiateDialog(PreviewZap)
						if self.previewActive:
							self.previewActive.show()
					self.hide()
				except:
					self.previewActive = None

	def menubuttonClick(self):
		if self.preview_zap or self.numberZapActive or self.FullEntryActive:
			return
		from .plugin import SetupZapSelectorScreen
		self.session.openWithCallback(self.cancelClick, SetupZapSelectorScreen)

	def greenbuttonClick(self):
		if self.preview_zap or self.numberZapActive or self.FullEntryActive:
			return
		if len(self.list) > 1:
			if config.plugins.SetupZapSelector.warning_message.value:
				self.session.openWithCallback(self.answerClear, MessageBox, _("Really clear history list ?"), type=MessageBox.TYPE_YESNO)
			else:
				self.answerClear(True)

	def answerClear(self, answer):
		if answer:
			from .plugin import InfoBarChannelSelection_instance, historyClear
			if InfoBarChannelSelection_instance and historyClear(InfoBarChannelSelection_instance):
				self.cancelClick()

	def deleteCurrentEntryClick(self):
		if self.preview_zap or self.numberZapActive or self.FullEntryActive:
			return
		cur_ref = self.getCurrent()
		if cur_ref and self.playservice and self.playservice != cur_ref:
			if config.plugins.SetupZapSelector.warning_message.value:
				self.session.openWithCallback(self.deleteEntryConfirmed, MessageBox, _("Really delete current entry ?"), type=MessageBox.TYPE_YESNO)
			else:
				self.deleteEntryConfirmed(True)

	def deleteEntryConfirmed(self, answer):
		if answer:
			from .plugin import InfoBarChannelSelection_instance, historyDeleteCurrentEntry
			ref = self.getCurrent()
			if InfoBarChannelSelection_instance and historyDeleteCurrentEntry(InfoBarChannelSelection_instance, ref):
				self.new_list = []
				cnt = 0
				for x in self.list:
					if x[0] != ref:
						if config.plugins.SetupZapSelector.number_zap.value:
							marker = "%d" % cnt
							if x[1] == "»":
								marker = "»"
							new_x = (x[0], marker, x[2], x[3], x[4], x[5], x[6], x[7])
							self.new_list.append(new_x)
						else:
							self.new_list.append(x)
						cnt += 1
				if len(self.list) > len(self.new_list):
					self["menu"].setList(self.new_list)
					new_title = _("History zap: count %d") % len(self.new_list)
					self.setTitle(new_title)
					if len(self.new_list) > 1:
						self["menu"].index = 1
					else:
						self["menu"].index = 0
					self.list = self.new_list

	def findPicon(self, service=None):
		if service is not None:
			sname = ':'.join(service.split(':')[:11])
			pos = sname.rfind(':')
			if pos != -1:
				sname = sname[:pos].rstrip(':').replace(':', '_')
				for path in self.searchPiconPaths:
					pngname = path + sname + ".png"
					if fileExists(pngname):
						return pngname
		return ""
