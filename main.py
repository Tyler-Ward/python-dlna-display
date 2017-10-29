
from Adafruit_CharLCD import Adafruit_CharLCDPlate


display = Adafruit_CharLCDPlate()

display.set_backlight(1)
display.message("DLNA Control\nInitilising")


import SOAPpy
import xml.etree.ElementTree
import time
import sys

server = SOAPpy.SOAPProxy(sys.argv[1]+"/upnp/control/rendertransport1",
        namespace = "urn:schemas-upnp-org:service:AVTransport:1")


while True:
    Position = server._sa("urn:schemas-upnp-org:service:AVTransport:1#GetPositionInfo").GetPositionInfo(InstanceID = 0)
    #Track = server._sa("urn:schemas-upnp-org:service:AVTransport:1#GetPositionInfo").GetPositionInfo(InstanceID = 0)

    #print Position.RelTime
    #print Position.TrackDuration
    #print Position.TrackMetaData

    namespaces = {"dc":"http://purl.org/dc/elements/1.1/"}

    try:
        trackData = xml.etree.ElementTree.fromstring(Position.TrackMetaData)
        trackName = trackData[0].find('dc:title',namespaces).text
        trackArtist = trackData[0].find('dc:creator',namespaces).text
    except xml.etree.ElementTree.ParseError:
        trackName = "Unknown"
        trackArtist = "Unknown"
    print trackName
   
    display.clear()
    display.home()
    display.message("%s\n%s/%s"%(trackName,Position.RelTime[2:],Position.TrackDuration[2:]))
    time.sleep(1)
