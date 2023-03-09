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
    
   
    
    # second_4_bits = int(mac[1], 16)
    # print(second_4_bits)
    # second_bin = decToBin(second_4_bits)
    # print(second_bin)
    
    
    
print("Please Select an Option: ")
print("1. MAC-Address to IPv6 Link-Local")
print("2. IPv6 Link-Local to MAC-Address")

select = input("Select: ")

if select == "1":
    print(mac2linklocal())    