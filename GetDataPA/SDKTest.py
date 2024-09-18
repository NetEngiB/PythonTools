from panos.firewall import Firewall
from getpass import getpass
import xml.etree.ElementTree as ET

#Auth Required
username=input('Enter username  :  ')
password=getpass()
ip=input('Enter IP address of Firewall  :  ')
#Firewall information for the SDK
fw1 = Firewall(ip,username,password)
#Run the command, assign to output
#The specific function varies based on the command
#.op commands are operational, like show ip arp or show jobs.
output=fw1.op('show system info',xml=True)
#turn output in to string
str_xml=str(output,encoding='utf-8')
#Assign parser to variable
xml_parser=ET.XMLParser()
#Parse the tree
xml_tree=ET.ElementTree(ET.fromstring(str_xml,xml_parser))

#Input the tags you'd like to return from the xml tree
#In this test, hostname, IP, serial number, and default gateway
wantedinfo=["hostname","ip-address","serial","default-gateway"]
#Iterate through wantedinfo[] and treat each item as "tag"
for tag in wantedinfo:
    #for each element in the xml tree
    for elem in xml_tree.iter():
        #if the element tag is the same as the item we're looking for from wantedinfo[], print in the format provided.
        if elem.tag==tag:
            print(elem.tag," : ",elem.text)

# Functionality Test : 09/18/2024 #