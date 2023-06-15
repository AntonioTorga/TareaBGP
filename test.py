import router as rt

ip_packet_v1 = "127.0.0.1,8885,10,347,0,00000005,1,hola!"

# print(rt.parse_packet(ip_packet_v1.encode()))
# print(rt.create_packet(rt.parse_packet(ip_packet_v1.encode()))==ip_packet_v1.encode())

# print(rt.read_line("127.0.0.1 8882 8885 127.0.0.1 8882 100"))

# print(rt.check_routes("v3_mtu/rutas_R2_v3_mtu.txt",("127.0.0.1",8885)))
# print(rt.check_routes("v3_mtu/rutas_R2_v3_mtu.txt",("127.0.0.1",8885)))

# print(rt.turn_to_string_eight(5))
# print(rt.turn_to_string_eight(500))
# print(rt.turn_to_string_eight(89922))

webada = rt.fragment_IP_packet(ip_packet_v1.encode(), 38)
print(webada)
for i in webada:
    print(rt.parse_packet(i)["MSG"],end="")
print()

