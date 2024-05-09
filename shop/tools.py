
def to_roman_numeral(value):
    roman_map = {                                   
        1: "I", 5: "V",
        10: "X", 50: "L",
        100: "C", 500: "D",
        1000: "M",
    }
    result = ""
    remainder = value

    for i in sorted(roman_map.keys(), reverse=True):
        if remainder > 0:
            multiplier = i
            roman_digit = roman_map[i]

            times = remainder // multiplier
            remainder = remainder % multiplier
            result += roman_digit * times

    return result