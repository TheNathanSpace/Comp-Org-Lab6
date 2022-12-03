def dec_to_bin(input: int, size: int) -> list:
    """
    Converts an int value to its binary representation (works for positive and negative numbers)
    :param input: The number to convert to binary
    :param size: The size of the number in bits
    :return: A list of single-character strings representing the number in binary (as a list, since in Python strings are immutable)
    """
    i: int = size - 1

    result = "0" * size
    result = list(result)

    onBit: str = '1'
    offBit: str = '0'
    if input < 0:
        input *= -1
        input -= 1
        onBit = '0'
        offBit = '1'

    while i != -1:
        quotient: int = int(input / 2)
        remainder: int = input % 2
        input = quotient
        if remainder == 1:
            result[i] = onBit
        else:
            result[i] = offBit
        i -= 1

    return result


def bin_to_dec(input: list) -> int:
    """
    Converts a binary number to decimal
    :param input: A binary number as a list of single-character strings
    :return: The converted decimal number as an int
    """
    i: int = len(input) - 1
    mul = 1
    dec = 0
    while True:
        dec += mul * int(input[i])
        mul *= 2
        i -= 1
        if i < 0:
            break
    return dec


def get_split_address(bin_address: list, tag_end_bit: int, index_end_bit: int, offset_end_bit: int):
    """
    Splits a binary address into its tag, index, and offset
    :param bin_address: The binary address as a list of single-character strings
    :param tag_end_bit: The index to stop slicing the block tag (since list indices start at 0,
                        this should be the number of tag bits)
    :param index_end_bit: The index to stop slicing the block index
    :param offset_end_bit: The index to stop slicing the block offset
    :return:
    """
    split_address = {}
    split_address["tag"] = bin_to_dec(bin_address[slice(0, tag_end_bit)])
    split_address["index"] = bin_to_dec(bin_address[slice(tag_end_bit, index_end_bit)])
    split_address["offset"] = bin_to_dec(bin_address[slice(index_end_bit, offset_end_bit)])
    return split_address


def split_dec_address(dec_address: int, tag_end_bit: int, index_end_bit: int, offset_end_bit: int):
    dec_address = dec_to_bin(dec_address, 32)
    split_addresses = get_split_address(bin_address = dec_address,
                                        tag_end_bit = tag_end_bit,
                                        index_end_bit = index_end_bit,
                                        offset_end_bit = offset_end_bit)
    tag: int = split_addresses["tag"]
    index: int = split_addresses["index"]
    offset: int = split_addresses["offset"]

    return tag, index, offset
