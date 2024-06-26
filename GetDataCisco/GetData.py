from netmiko import ConnectHandler
from getpass import getpass
import ipaddress


class GetData():
    def inactiveInterfaces(net_connect):
        '''
        Lists interfaces based on their connection status in "show interface status"

        Returns
        -------
            portlist[]

        Command for the list of ports is "sh int status | i notconnect"
        '''
        #Ports list buildout for later use
        ports=[]
        output=net_connect.send_command('sh int status | i notconnect')
        #Split output in to lines. Put each line in to a list of lines.
        lines=output.split('\n')
        #For each line in the list of lines
        for line in lines:
        #"words" is a bit misleading. This looks for spaces. There's a lot of spaces in the output here, so you get bits of blank output in the list of words. Ignore those
            words=line.split(' ')
            #Words[0] should ALWAYS be the interface as this is the first word in the output of the command above. Or at least it should be.
            #The below command removes leading and trailing spaces if any are present
            cleaned=words[0].strip()
            #Adds ports to the list of ports
            ports.append(cleaned)
        #Turn list in to tuple. Makes it so that I can pass "Portlist" and never change the structure of the list.
        portlist=tuple(ports)
        return(portlist)

    def lastInput(net_connect, ports):
        '''
        Takes a list of ports and returns the last input time.

        Returns
        --------
            portInput{}

        portInput{k:v}
        k=port
        v=time associated with "last input" in the command "sh in (port) | i hang"
        '''
        portInput={}
        for port in ports:
            line=net_connect.send_command(f'sh int {port} | i hang',use_textfsm=True)
            #Below - splits up the the bits of info from the above command and separates them in to parts['Last input x','last output y','output hang z'] list
            parts=line.split(', ')
            #Cleanup, removes leading spaces from the "last input x" list item
            Cleanup=parts[0].strip()
            #print(parts[0])
            #print(Cleanup)
            #Splits "last input x" in to bits['last','input','x']
            bits=Cleanup.split(' ')
            #Takes the third item in the bits list (which is the time of the last input) so that I can search for the last input time by port number
            portInput[port]=bits[2]
        return(portInput)

    def trunkCheck(net_connect, ports):
        '''
        Runs "sh run int {port} | i switchport mode" and returns the switchport mode on the interface.

        Ports that aren't set with a switchport mode will be checked further for proper configuration.

        If there's any trunk config, auto assigns port as "trunk". Otherwise, sets port value as "access"


        Returns
        --------
            items{}

        items{k:v}
        k=port
        v=mode
        '''
        items={}
        for port in ports:
            #Gets line of interface configuration that dictates "trunk" or "access"
            item=net_connect.send_command(f'sh run int {port} | i switchport mode')
            if item == '':
                #If the port is missing "switchport mode trunk" command, pull it out
                #Run 'sh run int {port} | i trunk' just to see if there's ANY trunk config
                #If not, continue as if the port is an access port
                CheckingTrunk=net_connect.send_command(f'sh run int {port} | i trunk')
                if CheckingTrunk == '':
                    mode='access'
                else:
                    mode='trunk'
            else:
                #Cleans up leading spaces
                cleaned=item.strip()
                #Splits in to ["switchport","mode","{trunk/access}"]
                pieces=cleaned.split(' ')
                #pieces[2] = "trunk" or "access"
                mode=pieces[2]
                #Create dictionary to see mode or port by port number
            items[port]=mode
        return(items)

    def getIpList():
        '''
        Reusable ip list grabber
        input IP address, check to make sure it's an IP address, add to list, return list

        Returns
        --------
            IPList

        Does not check for IP addresses in use in our environment, though you can write a ping test and append the list further if needed.
        '''
        IPList=[]
        while True:
            try:
                IPGrab=ipaddress.ip_address(input('Input a single IP address, or any other character  :  '))
                IPList.append(str(IPGrab))
                print('The current working list of IP Addresses is  :  ')
                print(IPList)
            except Exception as e:
                print(e)
                break
        IPList=tuple(IPList)
        return(IPList)

    def getSwitchUptime(net_connect):
        '''
        Checks for switch uptime by WEEKS. Runs "show version | i uptime"
        Does not return days, hours, or minutes. If the switch has been up for less than 1 week, returns 0

        Returns:
        --------------
        WeekCount - Integer

        Notes:
        ----------------
         * Can be easily checked against with "if WeekCount >= 1" style loops.
        '''
        Uptime=net_connect.send_command('sh ver | i uptime')
        if 'weeks' in Uptime:
            cleaned=Uptime.strip()
            bits=cleaned.split(' ')
            WeekCount=int(bits[3])
        else:
            WeekCount=0 
        return(WeekCount)

#Testing Function - pls ignore
def main():
    #Just testing getIpList here, I wouldn't recommend pushing the list to the IP of the test device for connection below.
    IPADD=GetData.getIpList()
    print('IP addresses that you entered')
    print(IPADD)
    for ip in IPADD:
        print(ip)
    #Test Device. One of our desk switches.
    #Check the IP before testing
    ip=IPADD
    Username=input('Input your username  :  ')
    password=getpass()
    device = {
    'device_type':'cisco_ios',
    'host': ip,
    'username': Username,
    'password': password,
    'secret': password,
    }
    net_connect=ConnectHandler(**device)
    ports=GetData.inactiveInterfaces(net_connect)
    for port in ports:
        print(f"{port} is inactive")
    lastInputs=GetData.lastInput(net_connect,ports)
    print(lastInputs)
    Modes=GetData.trunkCheck(net_connect,ports)
    print(Modes)
    for k,v in lastInputs.items():
        print(f"{k} last activity :  {v}")
    for k,v in Modes.items():
        print(f"{k} is a {v} port")
    GetData.getSwitchUptime(net_connect)

if __name__ == "__main__":
    main()