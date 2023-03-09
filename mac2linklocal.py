def bitFlipper(binary_string):
    if binary_string[-2] == "0":
        flip = "1"
        binary_string = binary_string[:-2] + flip + binary_string[-1]
    else:
        flip = "0"
        binary_string = binary_string[:-2] + flip + binary_string[-1]
    
    return binary_string


def decToBin(decimal_number):
    bin_format = ""
    
    if decimal_number <= 0:
        bin_format += "0000"
    elif decimal_number == 1:
        bin_format += "0001"
    else:
        bin_format += str(decToBin(decimal_number // 2))
        rest = decimal_number % 2
        bin_format += str(rest)
    
    
    return bin_format


def mac2linklocal():
    mac = input("Please Enter MAC-Address: ")
    
    first_hex_block = mac[0] + mac[1]
    
    second_nibble_in_dec = int(first_hex_block[1], 16)
    
    second_nibble_in_bin = decToBin(second_nibble_in_dec)[-4:]
    
    new_second_nibble_in_bin = bitFlipper(second_nibble_in_bin)
    
    second_nibble_back2hex = hex(int(new_second_nibble_in_bin,2)).lower()
    second_nibble_back2hex = second_nibble_back2hex[-1]
    
    if mac[1] != second_nibble_back2hex:
        new_character = str(second_nibble_back2hex)
        mac = mac[:1] + new_character + mac[2:]

    if len(mac) == 17:
        position = 8
        new_character = "-ff-fe-"
        mac = mac[:position] + new_character + mac[position+1:]

    counter = 5
    for i in range(len(mac)):
        if i == counter:
            position = counter
            new_character = ":"
            mac = mac[:position] + new_character + mac[position+1:]
            counter += 6
    
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
    second_bin = decToBin(second_4_bits)[-4:]
    second_bin = bitFlipper(second_bin)
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
