import json
import re

import xlwt

workBook = xlwt.Workbook()
workSheet = workBook.add_sheet('江寓房源')
title = ['id', '小区', '卧室', '朝向', '面积', '价格', '房间状态', '促销', '地铁', '地铁站点', '地铁距离',
         '楼层', '地址', '独卫', '阳台/飘窗']
for t in title:
    workSheet.write(0, title.index(t), t)


def serialize_data(room_data):
    id_ = room_data['id']
    bedroomNameAbbr = re.search(r"(.+)-卧室([0-9]+)", room_data['bedroomNameAbbr'])
    # # if bedroomNameAbbr:
    # #     xiaoqu, bed_room = bedroomNameAbbr.groups()
    # try:
    xiaoqu, bed_room = bedroomNameAbbr.groups()
    # except Exception as e:
    #     xiaoqu, bed_room = None, None
    #     print('bedroomNameAbbr', id_,room_data['bedroomNameAbbr'])
    # else:
    #     xiaoqu, bed_room = room_data['seoTitle'].split(' '), None
    chao_xiang = room_data['orientationName']
    mian_ji = room_data['usableArea']
    price = room_data['realityPrice']
    roomStatus = room_data['roomStatus']
    salesPromotion = room_data['salesPromotion']
    di_tie_data = re.search(r'距(.+号线)([\u4e00-\u9fa5]+)(\d+米)', room_data['trafficDistance'])
    if di_tie_data:
        di_tie, zhan_dian, ju_li = di_tie_data.groups()
    # try:
    #     di_tie, zhan_dian, ju_li = di_tie_data.groups()
    # except Exception as e:
    #     di_tie, zhan_dian, ju_li = None, None, None
    #     print("di_tie_data", id_, room_data['trafficDistance'])
    else:
        di_tie, zhan_dian, ju_li = None, None, None
    lou_cen = f"{room_data['floorNum']}/{room_data['floorTotal']}"
    di_zhi = room_data['premiseAddress']
    du_wei = None if room_data['hasToilet'] == '0' else '有'
    hasBalcony = room_data['hasBalcony']
    if hasBalcony == '1':
        hasBalcony = '阳台'
    elif hasBalcony == '2':
        hasBalcony = '飘窗'
    else:
        hasBalcony = None
    return [id_, xiaoqu, bed_room, chao_xiang, mian_ji, price, roomStatus, salesPromotion, di_tie, zhan_dian, ju_li,
            lou_cen, di_zhi, du_wei, hasBalcony]


with open('./room.json', 'r', encoding='utf-8') as f:
    roomData = json.load(f)

row = 1
for r in roomData:
    ser_data = serialize_data(r)
    for c in range(len(ser_data)):
        workSheet.write(row, c, ser_data[c])
    row += 1
workBook.save('江寓房源.xls')
