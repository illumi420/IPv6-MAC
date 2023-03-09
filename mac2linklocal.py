def mac2linklocal():
    mac = input("Please Enter MAC-Address: ")
    erste_octett = mac[0] + mac[1]
    #print(erste_octett)
    second_4_bits = int(mac[1], 16)
    #print(second_4_bits)
    second_bin = bin(second_4_bits)
    #print(second_bin)

    if len(second_bin) >= 3:
        if second_bin[-1] == "0":
            position = -2
            new_character = '0'
            second_bin = second_bin[:position] + new_character + second_bin[position+1:]

        if second_bin[-1] == "1":
            position = -2
            new_character = '1'
            second_bin = second_bin[:position] + new_character + second_bin[position+1]
    else:

        if second_bin[-2] == "0":
            position = -2
            new_character = '1'
            second_bin = second_bin[:position] + new_character + second_bin[position+1:]
            #print(second_bin)

        if second_bin[-2] == "1":
            position = -2
            new_character = '0'
            second_bin = second_bin[:position] + new_character + second_bin[position+1:]
            #print(second_bin)

    second_bin = int(second_bin, 2)
    second_bin = hex(second_bin).upper()
    second_4_bits = second_bin[2:]
    #print(second_4_bits)
    if mac[1] != second_4_bits:
        position = 1
        new_character = str(second_4_bits)
        mac = mac[:position] + new_character + mac[position+1:]

    if len(mac) == 17:
        position = 8
        new_character = "-FF-FE-"
        mac = mac[:position] + new_character + mac[position+1:]

    counter = 5
    for i in range(len(mac)):
        if i == counter:
            position = counter
            new_character = ":"
            mac = mac[:position] + new_character + mac[position+1:]
            counter += 6
    #print(mac)
    mac = mac.replace("-", "")

    return f"IPv6 Link-Local Address: " " fe80::"+mac.lower()


def linklocal2mac():
    ipv6 = input("Please Enter IPv6 Link-Local Address: ").upper()
    ipv6 = ipv6[6:]

    for i in range(len(ipv6)):
        if i == 2:
            ipv6 = ipv6[:2] + '-' + ipv6[2:]
        if i == 8:
            ipv6 = ipv6[:8] + '-' + ipv6[8:]
        if i == 14:
            ipv6 = ipv6[:14] + '-' + ipv6[14:]

    ipv6 = ipv6[:-2] + '-' + ipv6[-2:]
    ipv6 = ipv6.replace(":", "-")
    ipv6 = ipv6.replace("-FF-FE-", "-")

    second_4_bits = int(ipv6[1], 16)
    second_bin = bin(second_4_bits)
    #print(second_bin)

    if len(second_bin) >= 3:
        if second_bin[-1] == "0":
            position = -2
            new_character = '01'
            second_bin = second_bin[:position] + new_character + second_bin[position+1:]

        if second_bin[-1] == "1":
            position = -2
            new_character = '00'
            second_bin = second_bin[:position] + new_character + second_bin[position+1]
    else:

        if second_bin[-2] == "0":
            position = -2
            new_character = '1'
            second_bin = second_bin[:position] + new_character + second_bin[position+1:]
            #print(second_bin)

        if second_bin[-2] == "1":
            position = -2
            new_character = '0'
            second_bin = second_bin[:position] + new_character + second_bin[position+1:]
            #print(second_bin)

    second_bin = int(second_bin, 2)
    second_bin = hex(second_bin).upper()
    second_4_bits = second_bin[2:]

    if ipv6[1] != second_4_bits:
        position = 1
        new_character = str(second_4_bits)
        ipv6 = ipv6[:position] + new_character + ipv6[position+1:]
        ipv6 = ipv6

    return f"MAC-Address: "+ipv6


print("Please Select an Option: ")
print("1. MAC-Address to IPv6 Link-Local")
print("2. IPv6 Link-Local to MAC-Address")

select = input("Select: ")

if select == "1":
    print(mac2linklocal())

if select == "2":
    print(linklocal2mac())
