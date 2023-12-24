
class Args:
    def __init__(self, camera, cube):
        # 相机
        self.camera = camera
        # 长方体
        self.cube = cube


# 长方体参数
class Cube:
    def __init__(self, angles, disp, lwh):
        # 旋转角度
        self.angles = angles
        # 平移
        self.disp = disp
        # 长方体长宽高
        self.lwh = lwh


# 相机参数
class Camera:
    def __init__(self, f_len, sensor, reso, angle, place):
        # 分辨率
        self.reso = reso
        # 焦距
        self.f_len = f_len
        # 传感器尺寸
        self.sensor = sensor
        # 位置
        self.place = place
        # 角度
        self.angle = angle

