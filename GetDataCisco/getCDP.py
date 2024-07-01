import pandas as pd
from getpass import getpass
from netmiko import ConnectHandler


def getCDP(net_connect):
    '''
    This function runs "SH CDP NEIGHBORS DETAIL"
    It returns a set list of values right now in the form of a dataframe
    You may need the Pandas library to manipulate and utilze this function
    DOES NOT REMOVE WIRELESS ACCESS POINTS

    Returns
    -------
      destination_host, local_port, management_ip, remote_port

    Notes
    ------
    > Test cases available for adjustment. More values can be added to returns.

    > This output removes phones. I may add a function for getting phones if needed.

    > It removes phones, but doesn't fully remove their index in the dataframe.

    '''
    #Enable if needed
    net_connect.enable()
    #Run the command. Output = the command.
    output=net_connect.send_command('sh cdp neighbor detail',use_textfsm=True)
    #Below command in case you want to add more output to the initial df
    #print(output)
    #Convert to dataframe so that we can easily manipulate this data.
    df=pd.DataFrame(output)
    newdf=df[['destination_host','local_port','management_ip','remote_port']].copy()
    #print(newdf)
    #The line below removes phones from the output and dumps them in to a useless data frame.
    SwitchDF=newdf[newdf['destination_host'].str.contains("SEP")==False]
    #print(SwitchDF)
    return SwitchDF

def main():
    ##### FOR TESTING PURPOSES ######
    Username=input('Input your username  :  ')
    #Make sure to input an IP to test
    ip=''
    password=getpass()
    device = {
    'device_type':'cisco_ios',
    'host': ip,
    'username': Username,
    'password': password,
    'secret': password,
    }

    net_connect=ConnectHandler(**device)
    df=getCDP(net_connect)
    print(df)
   ##### FOR TESTING PURPOSES #######

if __name__ == '__main__':
    main()