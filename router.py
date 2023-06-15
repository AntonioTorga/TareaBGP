import sys
import socket

# router_ip = sys.argv[1]
# router_port = int(sys.argv[2])
# routes_path = sys.argv[3]
# buff_size = 1000
road_to = {}
def turn_to_string_eight(num):
    assert(type(num)==int)
    num = str(num)
    length = len(num)
    while length<8:
        num = "0"+num
        length+=1
    return num
def read_line(line):
    parsed_line = {}
    index = line.find(" ")
    parsed_line["IP_DESTINATION"] = line[:index]
    line= line[index+1:]
    index = line.find(" ")
    parsed_line["LOW_PORT"] = int(line[:index])
    line= line[index+1:]
    index = line.find(" ")
    parsed_line["HIGH_PORT"] = int(line[:index])
    line= line[index+1:]
    index = line.find(" ")
    parsed_line["IP_NEXT"] = line[:index]
    line= line[index+1:]
    index = line.find(" ")
    parsed_line["PORT_NEXT"] = int(line[:index])
    parsed_line["MTU"] = int(line[index+1:])
    return parsed_line
def parse_packet(ip_packet):
    ip_packet = ip_packet.decode()
    parsed_packet = {}
    index = ip_packet.find(",")
    parsed_packet["IP"] = ip_packet[:index]
    ip_packet= ip_packet[index+1:]
    index = ip_packet.find(",")
    parsed_packet["PORT"] = int(ip_packet[:index])
    ip_packet= ip_packet[index+1:]
    index = ip_packet.find(",")
    parsed_packet["TTL"] = int(ip_packet[:index])
    ip_packet= ip_packet[index+1:]
    index = ip_packet.find(",")
    parsed_packet["ID"] = int(ip_packet[:index])
    ip_packet= ip_packet[index+1:]
    index = ip_packet.find(",")
    parsed_packet["OFFSET"] = int(ip_packet[:index])
    ip_packet= ip_packet[index+1:]
    index = ip_packet.find(",")
    parsed_packet["SIZE"] = ip_packet[:index]
    ip_packet= ip_packet[index+1:]
    index = ip_packet.find(",")
    parsed_packet["FLAG"] = int(ip_packet[:index])
    parsed_packet["MSG"] = ip_packet[index+1:]
    return parsed_packet
def create_packet(parsed_packet):
    return (parsed_packet["IP"]+","+str(parsed_packet["PORT"])+","+str(parsed_packet["TTL"])+","+str(parsed_packet["ID"])+","+str(parsed_packet["OFFSET"])+","+parsed_packet["SIZE"]+","+str(parsed_packet["FLAG"])+","+parsed_packet["MSG"]).encode()
def check_routes(routes_file_name,destination_address):
    #si ya esta en la cache sacamos el primero, lo entregamos, y lo ponemos al final.(cola)
    if destination_address[1] in road_to:
        x = road_to[destination_address[1]].pop(0)
        road_to[destination_address[1]].append(x)
        return ((x[0],x[1]),x[2])
    # si no, pasamos a setear esta lista y retornar su primer elemento
    file = open(routes_file_name,"r")
    path = []
    while(True):
        data = file.readline()
        if not data:
            break
        data_parsed = read_line(data)
        if data_parsed["IP_DESTINATION"] == destination_address[0] and (data_parsed["LOW_PORT"]<=destination_address[1]<=data_parsed["HIGH_PORT"]):
            path.append((data_parsed["IP_NEXT"], data_parsed["PORT_NEXT"], data_parsed["MTU"]))
    if len(path)==0:
        return None
    x=path.pop(0) 
    path.append(x)
    road_to[destination_address[1]]=path
    return ((x[0],x[1]),x[2])
def fragment_IP_packet(ip_packet, MTU):
    length = len(ip_packet)
    if length <= MTU:
        return [ip_packet]
    
    parsed_packet = parse_packet(ip_packet)
    fragments = []
    message = parsed_packet["MSG"].encode()
    offset = parsed_packet["OFFSET"]
    header_size = length - int(parsed_packet["SIZE"])
    payload_size = MTU - header_size
    while(len(message) > 0):
        #create new packet
        flag = 1 if ((len(message) > payload_size) or parsed_packet["FLAG"]==1) else 0

        new_size = min(payload_size, len(message))
        
        new_offset = offset
        offset += new_size

        message_fragment = message[:new_size]
        message = message[new_size:]
        new_size = turn_to_string_eight(new_size)

        result = create_packet({"IP":parsed_packet["IP"],"PORT":parsed_packet["PORT"],"TTL":parsed_packet["TTL"],"ID":parsed_packet["ID"],"OFFSET":new_offset,"SIZE":new_size,"FLAG":flag,"MSG":message_fragment.decode()})
        fragments.append(result)
    
    return fragments
def reassemble_IP_packet(fragments):
    pass

# print(f"IP: {router_ip}, PORT: {router_port}")

# router_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# router_socket.bind((router_ip,router_port))

# while True:
#     og, add = router_socket.recvfrom(buff_size)
#     msg = parse_packet(og)
#     if msg["TTL"]==0:
#         print("Se recibió paquete {og} con TTL 0")
#         continue
#     if msg["IP"]==router_ip and msg["PORT"]==router_port:
#         print(msg["MSG"])
#     else:
#         tupla = check_routes(routes_path, (msg["IP"], msg["PORT"]))
#         if tupla == None:
#             print(f"No hay rutas hacia {msg['IP']} {msg['PORT']} para {og.decode()}")
#             continue
#         add, mtu = tupla
#         print(f"redirigiendo paquete {og} con destino final {(msg['IP'],msg['PORT'])} desde {(router_ip,router_port)} hacia {(add[0],add[1])}")
#         fragments = fragment_IP_packet(og, mtu)
#         for frag in fragments:
                #bajar TTL
#             router_socket.sendto(frag,(add[0],add[1]))

        

