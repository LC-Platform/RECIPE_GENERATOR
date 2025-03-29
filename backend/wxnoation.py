from wxconv import WXC

def convert_to_hindi(input_list):
    wx = WXC(order='wx2utf', lang='hin')
    wx1 = WXC(order='utf2wx', lang='hin')
    hindi_text_list = [wx1.convert(word) for word in input_list]
    return hindi_text_list

one_markers = ["meas_1"]
converted_text1 = convert_to_hindi(one_markers)
print(converted_text1)

