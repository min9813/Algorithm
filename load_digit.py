# coding:utf-8
import sys
import argparse

def main(string, index = 1, string_length = 0):
    index = string_length/5 * index
    print("index:",index)
    return count_digit_type(string, index = index, string_length=string_length)

def count_digit_type(string,_data_sum = 0, number = None, digit=1, index = 1, is_reverse = False,string_length = None):
    if digit ==1:
        is_reverse = string_length - index < index - _data_sum
        if is_reverse:
            _data_sum = string_length
    if is_reverse:
        print("逆に探索します.....")
        digit_list = ["9","8","7","6","5","4","3","2","1","0"]
    else:
        digit_list = ["0","1","2","3","4","5","6","7","8","9"]
    if digit >1:
        for k in range(len(digit_list)):
            digit_list[k] = number+digit_list[k]
    if digit > 20:
        sys.exit("stop")
    digit_sum = [0]*10
    data_sum = _data_sum
    letter_num = 0
    print("data_sum:",data_sum)
    for d in range(len(digit_list)):
        for k in range(string_length):
            if string[k:k+digit]==digit_list[d]:
                if is_reverse:
                    data_sum -= 1
                else:
                    data_sum += 1
                letter_num = k+1
        digit_sum[d] = data_sum
        print("digit_sum:",digit_sum)
        print("data_sum:",data_sum)
        print("_data_sum:",_data_sum)
        print(digit_list)
        if is_reverse:
            flag_next = data_sum <= index and _data_sum != data_sum
            flag_stop1 = 0<= index - digit_sum[d] and index - digit_sum[d] <=1
            if d>0:
                flag_stop2 = digit_sum[d] - digit_sum[d-1] == -1
            else:
                flag_stop2 = digit_sum[d] - _data_sum == -1
        else:
            flag_next = data_sum >= index and _data_sum != data_sum
            flag_stop1 = -1<= index - digit_sum[d] and index - digit_sum[d] <=0
            if d>0:
                flag_stop2 = digit_sum[d] - digit_sum[d-1] == 1
            else:
                flag_stop2 = digit_sum[d] - _data_sum == 1
        if flag_stop1 and flag_stop2:
            return digit_list[d],letter_num
        elif flag_next:
            if d > 0:
                if is_reverse:
                    flag_reverse = digit_sum[d-1] - index < index - digit_sum[d]
                    if flag_reverse: 
                        print("逆に探索します d > 0")
                        ans = count_digit_type(string, _data_sum = digit_sum[d-1], number = digit_list[d], digit = digit+1, index = index,is_reverse = True,string_length = string_length)
                        return ans
                    else:
                        ans = count_digit_type(string, _data_sum = digit_sum[d], number = digit_list[d], digit = digit+1, index = index,string_length=string_length)
                        return ans  
                else:
                    flag_reverse = data_sum - index < index - digit_sum[d-1]
                    if flag_reverse: 
                        print("逆に探索します d > 0")
                        ans = count_digit_type(string, _data_sum = data_sum, number = digit_list[d], digit = digit+1, index = index,is_reverse = True,string_length=string_length)
                        return ans                     
                    else:
                        ans = count_digit_type(string, _data_sum = digit_sum[d-1], number = digit_list[d], digit = digit+1, index = index,string_length=string_length)
                        return ans                    
            else:
                if is_reverse:
                    flag_reverse = _data_sum - index < index - digit_sum[d]
                    if flag_reverse: 
                        print("逆に探索します d > 0")
                        ans = count_digit_type(string, _data_sum = _data_sum, number = digit_list[d], digit = digit+1, index = index,is_reverse = True,string_length=string_length)
                        return ans
                    else:
                        ans = count_digit_type(string, _data_sum = digit_sum[d], number = digit_list[d], digit = digit+1, index = index,string_length = string_length)
                        return ans  
                else:
                    flag_reverse = data_sum - index < index - _data_sum
                    if flag_reverse: 
                        print("逆に探索します d > 0")
                        ans = count_digit_type(string, _data_sum = data_sum, number = digit_list[d], digit = digit+1, index = index,is_reverse = True,string_length=string_length)
                        return ans                     
                    else:
                        ans = count_digit_type(string, _data_sum = _data_sum, number = digit_list[d], digit = digit+1, index = index,string_length = string_length)
                        return ans
        else:
            pass
parser = argparse.ArgumentParser(
    prog = "show_digit.py",
    usage = "load n digit number and show n/5 * i (1<=i<=4)th number in dictoinary order.",
    description="description",
    epilog = "end",
    add_help = True,
)

parser.add_argument("load_file_name",help="load_file_name",
                            type=argparse.FileType("r"))
if __name__ =="__main__":
    args = parser.parse_args()
    digit_text = args.load_file_name.read().replace("\n","")
    args.load_file_name.close()
    index_list = [1,2,3,4]
    text_length = len(digit_text)
    print("text_length:",text_length)
    result = [main(digit_text,index=index,string_length = text_length) for index in index_list]
    print("--------result--------")    
    print(result)
    for index in index_list:
        print("{0} th digit : {1}".format((text_length/5)*index,result[index-1][1]))

