#coding=utf-8
import binascii
import requests
import time
import hashlib
import demjson
global url
iqi_post_url = "http://api.mirobot.com"
# voltage(int) 为电压, fb_value(int)为正反转 0为正转，1为反转
def buildVoltageMessage(voltage,fb_value):
    initMessage = [0 for i in range(12)]
    voltageMessage = bytearray(initMessage)
    voltageMessage[0] = "\x56"
    voltageMessage[1] = "\x03"
    voltageMessage[2] = "\x20"
    pwm = (int)((voltage/12)*4800)
    pwm_h = pwm/256
    pwm_l = pwm%256
    voltageMessage[3] = fb_value
    voltageMessage[4] = int(pwm_h)
    voltageMessage[5] = int(pwm_l)
    for index in range(len(voltageMessage)-2):
        voltageMessage[10] ^= voltageMessage[index]
    voltageMessage[11] = "\xaa"
    print binascii.hexlify(voltageMessage)
    return voltageMessage

#传入的数据应为回复的30个字节报文
#解析回复报文构建json数据传输给服务器
# 参数				参数值
# con             Motor
# act             get_parameter_list
# time			unix时间戳
# auth_code		校验值由con+act+time+‘MIROBOT’  md5生成
# is_publish		（1表示给正式用户使用，0表示给内侧用户使用）
#
# sn                   sn
# start_voltage        启动电压 0.8或者12
# start_current        启动电流
# work_current         工作电流
# rotate_speed         转速
# positive_pulse_wide  正脉宽
# negative_pulse_width 负脉宽
# phase_difference     相位差
# identification_pulse 识别脉冲
#转向                  正反
# result               结果
# {"error":0,"msg":"成功"}// 1:"参数错误"  2:"添加/更新失败"
def loadResponseMessage(sn_str,post_data_list):
    # messageBytearray = bytearray(binascii.unhexlify(reponseMessage))
    # print messageBytearray[1]
    #post 参数声明
    con = "con"
    con_data = "Motor"
    act = "act"
    act_data = "get_parameter_list"
    time_data = int(time.time())
    print time_data
    auth_code = "auth_code"
    md5 = hashlib.md5()
    md5.update(con_data + act_data + str(time_data) + 'MIROBOT')
    auth_code_data = md5.hexdigest()
    json_content = "json_content"
    #列表字典生成的json集合
    json = demjson.encode(post_data_list)
    print json
    #组建post 传输参数
    payload = {con: con_data, act: act_data, "time": time_data, auth_code: auth_code_data, "is_publish": "0","sn": sn_str, json_content:json}
    # 调用request 传输参数接口
    r = requests.post(iqi_post_url, data=payload)
    print (demjson.decode(r.text))
    return

#message_h 字节高八位，字节低八位，将其转换为整数
def messageConvertedInteger(message_h,message_l):
    return (ord(message_h)) * 256 + ord(message_l)
def messageConvertedVoltage(message_h,message_l):
    print "gao:"+str(message_h)+"-di:"+str(message_l)
    return float((float)(message_h * 256 + message_l)/(float)(4800)*12)
#sendMessage发送报文 receivedMessage 回复报文,返回一个装满参数的字典集合
def analyseReceivedMessage(sendMessage,receivedMessage):
    dict = {}
    # A口电机相位差
    phase_port_a = messageConvertedInteger(receivedMessage[2],receivedMessage[3])
    # B口电机相位差
    phase_port_b = messageConvertedInteger(receivedMessage[4],receivedMessage[5])
    #A口电机正负脉冲转速
    plus_pulse_speed_port_a = messageConvertedInteger(receivedMessage[6],receivedMessage[7])
    minus_pulse_speed_port_a = messageConvertedInteger(receivedMessage[8],receivedMessage[9])
    #B口电机正负脉冲转速
    plus_pulse_speed_port_b = messageConvertedInteger(receivedMessage[10],receivedMessage[11])
    minus_pulse_speed_port_b = messageConvertedInteger(receivedMessage[12], receivedMessage[13])
    # A口电机正脉冲宽度
    plus_pulse_width_port_a = messageConvertedInteger(receivedMessage[14],receivedMessage[15])
    # A口电机负脉冲宽度
    minus_pulse_width_port_a = messageConvertedInteger(receivedMessage[16],receivedMessage[17])
    # B口电机正脉冲宽度
    plus_pulse_width_port_b = messageConvertedInteger(receivedMessage[18], receivedMessage[19])
    # B口电机负脉冲宽度
    minus_pulse_width_port_b = messageConvertedInteger(receivedMessage[20], receivedMessage[21])
    #A+B 电流
    a_plus_b_current = messageConvertedInteger(receivedMessage[26], receivedMessage[27])
    dict['a_plus_b_current'] = a_plus_b_current
    #电机转速 =（ 正负脉冲转速*60）/24
     #A口电机转速
    plus_motor_speed_port_a = (plus_pulse_speed_port_a*60)/24
    minus_pulse_width_port_a = (minus_pulse_speed_port_a*60)/24
    dict['plus_motor_speed_port_a'] = plus_motor_speed_port_a
    dict['minus_pulse_width_port_a'] = minus_pulse_width_port_a
     #B口电机转速
    plus_motor_speed_port_b = (plus_pulse_speed_port_b*60)/24
    minus_motor_speed_port_b = (minus_pulse_speed_port_b*60)/24
    dict['plus_motor_speed_port_b'] = plus_motor_speed_port_b
    dict['minus_motor_speed_port_b'] = minus_motor_speed_port_b
    #脉宽占空比 =正负脉冲转速*正负脉宽/ 1000000
      #A口脉宽占空比
    plus_plus_pulse_width_occupy_empty_port_a =  plus_pulse_speed_port_a*plus_pulse_width_port_a/1000000
    plus_minus_pulse_width_occupy_empty_port_a = plus_pulse_speed_port_a*minus_pulse_width_port_a/1000000
    minus_plus_pulse_width_occupy_empty_port_a = minus_pulse_speed_port_a*plus_pulse_width_port_a/1000000
    minus_minus_pulse_width_occupy_empty_port_a = minus_pulse_speed_port_a*minus_pulse_width_port_a/1000000
    dict['plus_plus_pulse_width_occupy_empty_port_a'] = plus_plus_pulse_width_occupy_empty_port_a
    dict['plus_minus_pulse_width_occupy_empty_port_a'] = plus_minus_pulse_width_occupy_empty_port_a
    dict['minus_plus_pulse_width_occupy_empty_port_a'] = minus_plus_pulse_width_occupy_empty_port_a
    dict['minus_minus_pulse_width_occupy_empty_port_a'] = minus_minus_pulse_width_occupy_empty_port_a
      #B口脉宽占空比
    plus_plus_pulse_width_occupy_empty_port_b = plus_pulse_speed_port_b * plus_pulse_width_port_b / 1000000
    plus_minus_pulse_width_occupy_empty_port_b = plus_pulse_speed_port_b * minus_pulse_width_port_b / 1000000
    minus_plus_pulse_width_occupy_empty_port_b = minus_pulse_speed_port_b * plus_pulse_width_port_b / 1000000
    minus_minus_pulse_width_occupy_empty_port_b = minus_pulse_speed_port_b * minus_pulse_width_port_b / 1000000
    dict['plus_plus_pulse_width_occupy_empty_port_b'] = plus_plus_pulse_width_occupy_empty_port_b
    dict['plus_minus_pulse_width_occupy_empty_port_b'] = plus_minus_pulse_width_occupy_empty_port_b
    dict['minus_plus_pulse_width_occupy_empty_port_b'] = minus_plus_pulse_width_occupy_empty_port_b
    dict['minus_minus_pulse_width_occupy_empty_port_b'] = minus_minus_pulse_width_occupy_empty_port_b
    #相位差比例 = 相位差 / 正负脉冲宽度
      #分母为0不可除，抛出异常，此部分判断不严谨，后续整改
    if(plus_pulse_width_port_a!=0&minus_pulse_width_port_a!=0):
        # A口相位差比例
        plus_phase_difference_port_a = phase_port_a / plus_pulse_width_port_a
        minus_phase_difference_port_a = phase_port_a / minus_pulse_width_port_a
        # B口相位差比例
        plus_phase_difference_port_b = phase_port_b / plus_pulse_width_port_b
        minus_phase_difference_port_b = phase_port_b / minus_pulse_width_port_b

    else:
        plus_phase_difference_port_a = 0
        minus_phase_difference_port_a= 0
        plus_phase_difference_port_b = 0
        minus_phase_difference_port_b = 0
    dict['plus_phase_difference_port_a'] = plus_phase_difference_port_a
    dict['minus_phase_difference_port_a'] = minus_phase_difference_port_a
    dict['plus_phase_difference_port_b'] = plus_phase_difference_port_b
    dict['minus_phase_difference_port_b'] = minus_phase_difference_port_b
    dict['test_voltage'] = messageConvertedVoltage(sendMessage[4],sendMessage[5])
    dict['motor_turn'] = sendMessage[3]
    dict['test_result'] = ord(receivedMessage[1])
    return dict
#参数为回复报文集合
def checkIsSuccess(post_data_list):
    i=0
    if(len(post_data_list)>0&len(post_data_list)<=4):
     for index in range(len(post_data_list)):
         if((int)(post_data_list[index]['test_result'])!=2):
             return False
         else:
             i+=1
     if(i==4):
         return True
    return False
