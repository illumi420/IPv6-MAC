class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def verbose(user_select):
    print()
    print("#" * 72)
    print(
        f"# a {bcolors.YELLOW}MAC-Address{bcolors.ENDC} is 48 bits, an {bcolors.OKBLUE}IPv6 Address{bcolors.ENDC} is 128 bits"
    )
    print("# so what happend is as follows: ")
    if user_select == "1":
        print(f"# from the {bcolors.YELLOW}MAC-Address{bcolors.ENDC} ", initial_mac)
        print(f"# take the first hex octet ", first_hex_block)
        print(
            f"# take the {bcolors.RED}second nibble{bcolors.ENDC} of that first hex octet {first_hex_block[0]}{bcolors.RED}{first_hex_block[1]}{bcolors.ENDC}"
        )
        print(
            f"# convert that {bcolors.RED}second nibble{bcolors.ENDC} into binary string",
            second_nibble_in_bin,
        )
        print(f"# flip/invert the most significant bit in that binary string")
        print(
            f"# {second_nibble_in_bin[:2]}{bcolors.RED}{second_nibble_in_bin[-2]}{bcolors.ENDC}{second_nibble_in_bin[-1]} => {new_second_nibble_in_bin[:2]}{bcolors.OKGREEN}{new_second_nibble_in_bin[-2]}{bcolors.ENDC}{new_second_nibble_in_bin[-1]} now convert the new binary string back to hex"
        )
        print(
            f"# {new_second_nibble_in_bin} => {second_nibble_back2hex} this is the new first hex octet {mid_initial_mac[0]}{bcolors.OKGREEN}{mid_initial_mac[1]}{bcolors.ENDC}"
        )
        print("# reformat to IPv6 notation: replace '-'s with ':'s   ")
        print("# append ff:fe in the middle")
        print("# readjust the hex blocks into 16-bit per block format")
        print("# prepend the fe80:: Link-Local prefix")
        print("#" * 72)
        print()

    if user_select == "2":
        print(
            f"# from the {bcolors.OKBLUE}Link-Local Address{bcolors.ENDC}", initial_ipv6
        )
        print(
            "# reformat to MAC notation: remove the Link-Local prefix fe80:: and the ff:fe from the middle"
        )
        print(
            f"# replace the ':'s with '-'s readjust the hex blocks into 8-bit per block format",
            mid_ipv6,
        )
        print(
            f"# from the first hex block {mid_ipv6[:2]} take the {bcolors.OKGREEN}second nibble{bcolors.ENDC} {mid_ipv6[0]}{bcolors.OKGREEN}{mid_ipv6[1]}{bcolors.ENDC} and convert it to binary {second_bin}"
        )
        print(
            f"# from that binary string flip/invert the most significant bit {second_bin[:2]}{bcolors.OKGREEN}{second_bin[-2]}{bcolors.ENDC}{second_bin[-1]} => {mid_second_bin[:2]}{bcolors.RED}{mid_second_bin[-2]}{bcolors.ENDC}{mid_second_bin[-1]}"
        )
        print(
            f"# convert the {bcolors.RED}new binary string{bcolors.ENDC} {mid_second_bin} back to hex => {bcolors.RED}{second_4_bits}{bcolors.ENDC} then rebuild the first hex octet {mid_ipv6[0]}{bcolors.RED}{last_ipv6[1]}{bcolors.ENDC}"
        )
        print("#" * 72)
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
    initial_mac = input(f"# Please Enter {bcolors.YELLOW}MAC-Address:{bcolors.ENDC} ")

    global first_hex_block
    first_hex_block = initial_mac[0] + initial_mac[1]

    second_nibble_in_dec = int(first_hex_block[1], 16)

    global second_nibble_in_bin
    second_nibble_in_bin = decToBin(second_nibble_in_dec)[-4:]

    global new_second_nibble_in_bin
    new_second_nibble_in_bin = bitFlipper(second_nibble_in_bin)

    global second_nibble_back2hex
    second_nibble_back2hex = hex(int(new_second_nibble_in_bin, 2)).lower()
    second_nibble_back2hex = second_nibble_back2hex[-1]

    if initial_mac[1] != second_nibble_back2hex:
        new_character = str(second_nibble_back2hex)
        global mid_initial_mac
        mid_initial_mac = initial_mac[:1] + new_character + initial_mac[2:]

    if len(mid_initial_mac) == 17:
        position = 8
        new_character = "-ff-fe-"
        mid_initial_mac = (
            mid_initial_mac[:position] + new_character + mid_initial_mac[position + 1 :]
        )

    counter = 5
    for i in range(len(mid_initial_mac)):
        if i == counter:
            position = counter
            new_character = ":"
            mid_initial_mac = (
                mid_initial_mac[:position]
                + new_character
                + mid_initial_mac[position + 1 :]
            )
            counter += 6

    ipv6 = mid_initial_mac.replace("-", "")

    return (
        f"# {bcolors.OKBLUE}IPv6 Link-Local Address:{bcolors.ENDC} "
        " fe80::" + ipv6.lower()
    )


def linklocal2mac():
    global initial_ipv6
    initial_ipv6 = input(
        f"# Please Enter {bcolors.OKBLUE}IPv6 Link::Local Address:{bcolors.ENDC} "
    ).lower()

    global deformed_ipv6
    deformed_ipv6 = initial_ipv6[6:]

    for i in range(len(deformed_ipv6)):
        if i == 2:
            deformed_ipv6 = deformed_ipv6[:2] + "-" + deformed_ipv6[2:]
        if i == 8:
            deformed_ipv6 = deformed_ipv6[:8] + "-" + deformed_ipv6[8:]
        if i == 14:
            deformed_ipv6 = deformed_ipv6[:14] + "-" + deformed_ipv6[14:]

    global mid_ipv6
    mid_ipv6 = deformed_ipv6[:-2] + "-" + deformed_ipv6[-2:]
    mid_ipv6 = mid_ipv6.replace(":", "-")
    mid_ipv6 = mid_ipv6.replace("-ff-fe-", "-")

    global second_4_bits
    second_4_bits = int(mid_ipv6[1], 16)
    global second_bin
    second_bin = decToBin(second_4_bits)[-4:]
    global mid_second_bin
    mid_second_bin = bitFlipper(second_bin)
    new_mid_second_bin = int(mid_second_bin, 2)
    second_hex = hex(new_mid_second_bin).lower()

    second_4_bits = second_hex[2:]

    if mid_ipv6[1] != second_4_bits:
        position = 1
        new_character = str(second_4_bits)
        global last_ipv6
        last_ipv6 = mid_ipv6[:position] + new_character + mid_ipv6[position + 1 :]
        mac = last_ipv6

    return (
        "#" + " " * 14 + f"{bcolors.YELLOW}MAC-Address:{bcolors.ENDC} " + " " * 13 + mac
    )


print("Please Select an Option: ")
print(
    f"1. {bcolors.YELLOW}MAC-Address{bcolors.ENDC} to {bcolors.OKBLUE}IPv6 Link::Local{bcolors.ENDC}"
)
print(
    f"2. {bcolors.OKBLUE}IPv6 Link::Local{bcolors.ENDC} to {bcolors.YELLOW}MAC-Address{bcolors.ENDC}"
)

select = input("Select: ")
print()
print("#" * 72)

if select == "1":
    print(mac2linklocal())

if select == "2":
    print(linklocal2mac())

print("#" * 72)
verbose(select)
