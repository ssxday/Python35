from PIL import Image, ExifTags

me = Image.open('me.jpg')
me1 = Image.open('me1.jpg')

print(me)
for k, v in me.info.items():
    print(k, '\t', v)

print()
# 使用_getexif()方法：
print('使用_getexif()方法：')
exif = me._getexif()
print(exif)
print('信息替代后：')

def recoverexif(exif):
    recovery = dict()
    for i, v in exif.items():
        j = ExifTags.TAGS[i]
        recovery[j] = v
    return recovery

recovery = recoverexif(exif)
print(recovery)

for k,v in recovery.items():
    print(k,':\t',v)

# 用ps修过后的exif,46项
exif_after_ps = {'BitsPerSample': (8, 8, 8), 'YResolution': (720000, 10000), 'FocalLengthIn35mmFilm': 31, 'SamplesPerPixel': 3, 'ISOSpeedRatings': 200, 'SensingMethod': 2, 'MeteringMode': 5, 'Flash': 32, 'XResolution': (720000, 10000), 'ImageLength': 1280, 'Model': 'iPhone 6 Plus', 'ImageWidth': 960, 'FocalLength': (53, 20), 'ComponentsConfiguration': b'\x01\x02\x03\x00', 'SubsecTimeDigitized': '009', 'FNumber': (11, 5), 'ExifImageHeight': 720, 'Make': 'Apple', 'ExposureProgram': 2, 'PhotometricInterpretation': 2, 'ExifVersion': b'0221', 'ExifOffset': 304, 'Orientation': 1, 'LensMake': 'Apple', 'ExposureTime': (1, 33), 'ColorSpace': 1, 'SceneType': b'\x01', 'LensSpecification': ((53, 20), (53, 20), (11, 5), (11, 5)), 'GPSInfo': {1: 'N', 2: ((22, 1), (30, 1), (5109, 100)), 3: 'E', 4: ((113, 1), (55, 1), (1988, 100)), 5: b'\x00', 6: (13878, 965), 7: ((5, 1), (38, 1), (4400, 100)), 12: 'K', 13: (0, 1), 16: 'M', 17: (27384, 361), 23: 'M', 24: (30191, 118), 29: '2016:12:19', 31: (30, 1)}, 'SubsecTimeOriginal': '009', 'YCbCrPositioning': 1, 'BrightnessValue': (10126, 5233), 'DateTime': '2016:12:19 14:05:59', 'WhiteBalance': 0, 'Software': 'Adobe Photoshop CC 2015 (Macintosh)', 'DateTimeDigitized': '2016:12:19 13:38:45', 'FlashPixVersion': b'0100', 'LensModel': 'iPhone 6 Plus front camera 2.65mm f/2.2', 'DateTimeOriginal': '2016:12:19 13:38:45', 'ExposureMode': 0, 'SceneCaptureType': 0, 'ShutterSpeedValue': (8504, 1681), 'ExifImageWidth': 960, 'ExposureBiasValue': (0, 1), 'ResolutionUnit': 2, 'ApertureValue': (7983, 3509)}
# Ps修前的exif,42项
exif_before_ps = {'LensSpecification': ((53, 20), (53, 20), (11, 5), (11, 5)), 'ISOSpeedRatings': 200, 'ExifVersion': b'0221', 'SubsecTimeDigitized': '009', 'FNumber': (11, 5), 'MakerNote': b'Apple iOS\x00\x00\x01MM\x00\t\x00\x01\x00\t\x00\x00\x00\x01\x00\x00\x00\x04\x00\x03\x00\x07\x00\x00\x00h\x00\x00\x00\x80\x00\x04\x00\t\x00\x00\x00\x01\x00\x00\x00\x01\x00\x05\x00\t\x00\x00\x00\x01\x00\x00\x00\xb8\x00\x06\x00\t\x00\x00\x00\x01\x00\x00\x00\xaf\x00\x07\x00\t\x00\x00\x00\x01\x00\x00\x00\x01\x00\x08\x00\n\x00\x00\x00\x03\x00\x00\x00\xe8\x00\x0e\x00\t\x00\x00\x00\x01\x00\x00\x00\x00\x00\x14\x00\t\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00bplist00\xd4\x01\x02\x03\x04\x05\x06\x07\x08UflagsUvalueUepochYtimescale\x10\x01\x13\x00\x05%j\xdbz\xffr\x10\x00\x12;\x9a\xca\x00\x08\x11\x17\x1d#-/8:\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xff\xff\xff\xb5\x00\x00\x1c\x9f\xff\xff\xf6\x92\x00\x00\t\x91\x00\x00\x00U\x00\x00\xfd\x8f', 'ApertureValue': (7983, 3509), 'ExifImageHeight': 960, 'ResolutionUnit': 2, 'ExposureProgram': 2, 'GPSInfo': {1: 'N', 2: ((22, 1), (30, 1), (5109, 100)), 3: 'E', 4: ((113, 1), (55, 1), (1988, 100)), 5: b'\x00', 6: (13878, 965), 7: ((5, 1), (38, 1), (4400, 100)), 12: 'K', 13: (0, 1), 16: 'M', 17: (27384, 361), 23: 'M', 24: (30191, 118), 29: '2016:12:19', 31: (30, 1)}, 'Flash': 32, 'DateTimeDigitized': '2016:12:19 13:38:45', 'YCbCrPositioning': 1, 'WhiteBalance': 0, 'DateTime': '2016:12:19 13:38:45', 'ExposureBiasValue': (0, 1), 'SceneType': b'\x01', 'YResolution': (72, 1), 'BrightnessValue': (10126, 5233), 'FocalLengthIn35mmFilm': 31, 'ExposureTime': (1, 33), 'Make': 'Apple', 'XResolution': (72, 1), 'ExifImageWidth': 1280, 'ExposureMode': 0, 'SubsecTimeOriginal': '009', 'Model': 'iPhone 6 Plus', 'Software': '10.1.1', 'SensingMethod': 2, 'Orientation': 6, 'DateTimeOriginal': '2016:12:19 13:38:45', 'LensMake': 'Apple', 'ComponentsConfiguration': b'\x01\x02\x03\x00', 'FocalLength': (53, 20), 'FlashPixVersion': b'0100', 'ShutterSpeedValue': (8504, 1681), 'SceneCaptureType': 0, 'ExifOffset': 210, 'LensModel': 'iPhone 6 Plus front camera 2.65mm f/2.2', 'ColorSpace': 1, 'MeteringMode': 5}

print('afterPS',len(exif_after_ps.values()))
print('beforePS',len(exif_before_ps.keys()))
# 开始对比的流程：
print('开始对比的流程：')

def differs(l1,l2):
    cha = dict()
    cha[0] = list(l1 - l2)
    cha[1] = list(l2 - l1)
    return cha


# cha = exif_before_ps.keys() - exif_after_ps.keys()
print('差：')
cha = differs(exif_before_ps.keys(),exif_after_ps.keys())
print(cha)
print()
print('MakerNote:',exif_before_ps['MakerNote'])
for i in cha[1]:
    print(i,':',exif_after_ps[i])

jielun = 'ps前，图像有MakerNote信息，ps后该信息丢失。\n' \
         'ps后，图像添加了5个属性，分别是：\n' \
         'BitsPerSample : (8, 8, 8)'



