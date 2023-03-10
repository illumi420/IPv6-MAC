class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def verbose(user_select):
    print()
    print()
    print("#"*72)
    print(f"# a {bcolors.YELLOW}MAC-Address{bcolors.ENDC} is 48 bits, an {bcolors.OKBLUE}IPv6 Address{bcolors.ENDC} is 128 bits")
    print("# so what happend is as follows: ")
    if user_select == "1":
        print(f"# from the {bcolors.YELLOW}MAC-Address{bcolors.ENDC} ", initial_mac)
        print(f"# take the first hex octet ",first_hex_block)
        print(f"# take the {bcolors.RED}second nibble{bcolors.ENDC} of that first hex octet {first_hex_block[0]}{bcolors.RED}{first_hex_block[1]}{bcolors.ENDC}")
        print(f"# convert that {bcolors.RED}second nibble{bcolors.ENDC} into binary", second_nibble_in_bin)
        print(f"# flip/invert the most significant bit in that binary")
        print(f"# {second_nibble_in_bin[:2]}{bcolors.RED}{second_nibble_in_bin[-2]}{bcolors.ENDC}{second_nibble_in_bin[-1]} => {new_second_nibble_in_bin[:2]}{bcolors.OKGREEN}{new_second_nibble_in_bin[-2]}{bcolors.ENDC}{new_second_nibble_in_bin[-1]} now convert the new binary back to hex")
        print(f"# {new_second_nibble_in_bin} => {second_nibble_back2hex} this is the new first hex octet {mid_initial_mac[0]}{bcolors.OKGREEN}{mid_initial_mac[1]}{bcolors.ENDC}")
        print("# reformat to IPv6 notation: replace '-'s with ':'s   ")
        print("# append ff:fe in the middle")
        print("# readjust the hex blocks into 16-bit per block format")
        print("# prepend the fe80:: Link-Local prefix")
        print("#"*72)
        print()

def bitFlipper(binary_string):
    if binary_string[-2] == "0":
        flip = "1"
        binary_string = binary_string[:-2] + flip + binary_string[-1]
    else:
        flip = "0"
        binary_string = binary_string[:-2] + flip + binary_string[-1]
    
    return binary_string



def decToBin(decimal_number):
    global bin_format
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
    global initial_mac
    initial_mac = input(f"Please Enter {bcolors.YELLOW}MAC-Address:{bcolors.ENDC} ")
    
    global first_hex_block
    first_hex_block = initial_mac[0] + initial_mac[1]
    
    second_nibble_in_dec = int(first_hex_block[1], 16)
    
    global second_nibble_in_bin
    second_nibble_in_bin = decToBin(second_nibble_in_dec)[-4:]
    
    global new_second_nibble_in_bin
    new_second_nibble_in_bin = bitFlipper(second_nibble_in_bin)
    
    global second_nibble_back2hex
    second_nibble_back2hex = hex(int(new_second_nibble_in_bin,2)).lower()
    second_nibble_back2hex = second_nibble_back2hex[-1]
    
    if initial_mac[1] != second_nibble_back2hex:
        new_character = str(second_nibble_back2hex)
        global mid_initial_mac 
        mid_initial_mac = initial_mac[:1] + new_character + initial_mac[2:]

    if len(mid_initial_mac) == 17:
        position = 8
        new_character = "-ff-fe-"
        mid_initial_mac = mid_initial_mac[:position] + new_character + mid_initial_mac[position+1:]

    counter = 5
    for i in range(len(mid_initial_mac)):
        if i == counter:
            position = counter
            new_character = ":"
            mid_initial_mac = mid_initial_mac[:position] + new_character + mid_initial_mac[position+1:]
            counter += 6
    
    new_mac = mid_initial_mac.replace("-", "")

    return f"{bcolors.OKBLUE}IPv6 Link-Local Address:{bcolors.ENDC} " " fe80::"+new_mac.lower()



def linklocal2mac():
    ipv6 = input(f"Please Enter {bcolors.OKBLUE}IPv6 Link::Local Address:{bcolors.OKBLUE} ").upper()
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

    return f"{bcolors.YELLOW}MAC-Address:{bcolors.ENDC} "+ipv6


print("Please Select an Option: ")
print(f"1. {bcolors.YELLOW}MAC-Address{bcolors.ENDC} to {bcolors.OKBLUE}IPv6 Link-Local{bcolors.ENDC}")
print(f"2. {bcolors.OKBLUE}IPv6 Link-Local{bcolors.ENDC} to {bcolors.YELLOW}MAC-Address{bcolors.ENDC}")

select = input("Select: ")
print()

if select == "1":
    print(mac2linklocal())

if select == "2":
    print(linklocal2mac())

verbose(select)