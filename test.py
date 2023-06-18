def create_BGP_message(routes):
    msg = "BGP_ROUTES\n"+str(8881)
    for end,route in routes.items():
        route = [str(x) for x in route]
        msg += "\n"+" ".join(route)
    msg += "\n"+"END_ROUTES"
    return msg.encode()

routes = {8885:[8885,8882,8881],8884:[8884,8883,8881],8885:[8885,8884,8881]}
print(create_BGP_message(routes).decode())