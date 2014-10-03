__author__ = '1975andy'

# fun parseInterfaces (switch_ports)
#          input param var switch_ports String
#          return var rep_ports List
# Cisco: example switch_port = "1/1,1/2,1/3-1/6,1/7,1/10"
#                return rep_ports =['1/1','1/2','1/3','1/4','1/5','1/6','1/7','1/10']
#
# Arista: example switch_port = "1,2,3-6,7,10"
#                return rep_ports =['1','2','3','4','5','6','7','10']


rep_cisco_ports = "1/1,1/3-1/20"
rep_arista_ports = "1,2,3,4-8,20-60"

def parseInterfaces ( switch_ports ):

    rep_ports = []

    print '\n'
    print str(switch_ports) + '\n'
    switch_ports = switch_ports.split(',')
    print str(switch_ports) + '\n'

    for ports in switch_ports:

        if "-" in ports:
            ports=ports.split('-')

            if ports[0].find('/') >= 0:
                i =  int(ports[0][ports[0].find('/')+1:])

                while i != int(ports[1][ports[1].find('/')+1:])+1:
                    rep_ports.append(str(ports[0][:ports[0].find('/')]) + '/' + str(i))
                    i += 1
            else:
                i =  int(ports[0])

                while i != int(ports[1])+1:
                    rep_ports.append(str(i))
                    i += 1
        else:
            rep_ports.append(ports)

    return rep_ports

def main():
    print parseInterfaces ( rep_arista_ports )
    print '\n'
    print parseInterfaces ( rep_cisco_ports )

if __name__ == "__main__":
    main()