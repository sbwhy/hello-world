#coding=utf-8
import binascii
import requests
import time
import hashlib
import demjson
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
def loadResponseMessage(reponseMessage):
    messageBytearray = bytearray(binascii.unhexlify(reponseMessage))
    print messageBytearray[1]
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
    #声明一个空的列表
    list_recive_content_data = []
    #根据护肤报文生成python 字典集合
    recive_content_data = {"start_voltage": "13", "start_current": "34", "work_current": "34","rotate_speed": "34", "positive_pulse_wide": "34", "negative_pulse_width": "34","phase_difference": "34","identification_pulse": "34", "result": "1"}
    #往list添加每次回复报文生成的字典，
    list_recive_content_data.append(recive_content_data)
    list_recive_content_data.append(recive_content_data)
    list_recive_content_data.append(recive_content_data)
    list_recive_content_data.append(recive_content_data)
    #列表字典生成的json集合
    json = demjson.encode(list_recive_content_data)
    print json
    #组建post 传输参数
    payload = {con: con_data, act: act_data, "time": time_data, auth_code: auth_code_data, "is_publish": "0","sn": "161229495351", json_content:json}
    # 调用request 传输参数接口
    r = requests.post("http://api.mirobot.com", data=payload)
    print (demjson.decode(r.text))
    return