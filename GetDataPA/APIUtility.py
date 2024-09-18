import requests
from getpass import getpass
import xml.etree.ElementTree as ET
import pandas as pd

#username=input('Enter username  :  ')
#password=getpass()

def xml_to_dict(response):
    """
    Parses XML output from Palo API and spits out a dictionary to be utilized later
    Requires the xml response from the API query. Functions with base response, no further xml work needed.

    You can print the dictionary to see results and pull the values you want in your own script.
    Outputs may vary based on input
    DOES NOT WORK WITH PANOS SDK OUTPUT, MUST BE XML FROM API
    """
    #Dictionary for buildout later
    xml_dict={}
    #Assign parser
    xml_parser=ET.XMLParser()
    #XML output to variable, parsed
    xml_tree=ET.ElementTree(ET.fromstring(response.text,xml_parser))
    #pull the info out 
    for xml_dig in xml_tree.iter():
        k=xml_dig.tag
        v=xml_dig.text
        xml_dict[k]=v
    return(xml_dict)


def main():
    """
    Used for testing of the individual functions
    Includes examples for inputs needed for the functions above
    """
    #To pull specific Palo API URLs, use the "https://{palo device}/api" web gui to find what you want.
    #Once you've found the request you want to get responses from, the Palo device should give you a url as well.
    #The url shoul look like "/api/?type=...", and you'd just add it to the end of your existing URL from above.
    #The response line below is for example purposes only. The IP address is not real and the auth credentials should be your own
    showarp=requests.get("https://{firewall}/api/?type=op&cmd=<show><arp><entry name = 'all'/></arp></show>",auth=({username},{password}), verify=False)
    showjobs=requests.get("https://{firewall}/api/?type=op&cmd=<show><jobs><all></all></jobs></show>",auth=({username},{password}), verify=False)
    #print(response.status_code)
    #^to test http get response^#
    xdict=xml_to_dict(showarp)
    ydict=xml_to_dict(showjobs)
    print(ydict)
    print(xdict)
    #One way to utilize this dict is to use a python library like "pandas" to present audits of information
    print('show arp all')
    df1=pd.DataFrame.from_dict(xdict,orient='index')
    print(df1)
    print('show jobs all')
    df2=pd.DataFrame.from_dict(ydict,orient="index")
    print(df2)
    #Once you've got the dataframes, it's pretty easy to run .to_excel or .to_csv functions to spit out the info you want.


if __name__ == "__main__":
    main()

# Functionality Test : 09/18/2024 #