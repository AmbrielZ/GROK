from fff import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QButtonGroup, QAbstractButton, QFileSystemModel
import sys
from PyQt5.QtGui import *
import cv2
from PyQt5.QtCore import QTimer, Qt
import socket
import os
from threading import Thread


class GrokFormMsg:
    def __init__(self, mob, node_type="Cycle", font_color="#00FFFF", node_color="#FF7AB2",
                 node_size=60, label=0, play_rate=50):
        self.mob = mob  # 设置的结构体类型
        self.node_type = node_type  # 节点类型
        self.font_color = font_color  # 字体颜色
        self.node_color = node_color  # 节点颜色
        self.node_size = node_size / 100.0  # 节点大小
        self.label = label  # 是否开启说明 比如push的时候显示push:xx
        self.play_rate = play_rate / 100.0  # 播放速度

    def change_node_type(self, ntype):
        self.node_type = ntype

    def change_node_color(self, ncolor):
        self.node_color = ncolor

    def change_font_color(self, fcolor):
        self.font_color = fcolor

    def label_on(self):
        self.label = 1

    def label_off(self):
        self.label = 0

    def set_size(self, node_size):
        self.node_size = node_size / 100.0

    def set_rate(self, play_rate):
        self.play_rate = play_rate / 100.0


GrokFormMsg_vector = GrokFormMsg("vector")
GrokFormMsg_TreeHeap = GrokFormMsg("TreeHeap")
GrokFormMsg_ArrHeap = GrokFormMsg("ArrHeap")
GrokFormMsg_stack = GrokFormMsg("stack")
GrokFormMsg_Tree = GrokFormMsg("Tree")


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mod = "vector"
        self.gfmsg = GrokFormMsg_vector
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.frame_2.setCursor(Qt.SizeHorCursor)
        self.ui.frame_3.setCursor(Qt.SizeVerCursor)
        self.ui.frame_6.setCursor(Qt.SizeFDiagCursor)
        self.ui.pushButton_max.clicked.connect(self.restore_or_maximize_window)
        self.model01 = QFileSystemModel()
        self.model01.setRootPath('')
        self.model01.setNameFilterDisables(False)  # 过滤掉的灰色文件不显示
        self.model01.setNameFilters(['*.mp4'])
        self.ui.treeView.setModel(self.model01)
        for col in range(1, 4):
            self.ui.treeView.setColumnHidden(col, True)
        self.ui.treeView.doubleClicked.connect(self.initUI)
        self.f_type = 0
        self.evn = 4
        self.showgfmsg()
        self.ui.horizontalSlider.setRange(0, 1000)
        self.ui.pushButton_back.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(False)
        self.ui.pushButton_forward.setEnabled(False)
        self.ui.horizontalSlider.setEnabled(False)
        self.btn_group = QButtonGroup(self)
        self.btn_group.addButton(self.ui.pushButton_vector, 0)
        self.btn_group.addButton(self.ui.pushButton_stack, 1)
        self.btn_group.addButton(self.ui.pushButton_heap, 2)
        self.btn_group.addButton(self.ui.pushButton_tree, 3)
        self.btn_group.buttonClicked[QAbstractButton].connect(self.set_gfmsg)
        self.ui.comboBox_yangshi.currentIndexChanged.connect(self.change_form_inputs)
        self.ui.comboBox_label.currentIndexChanged.connect(self.setbtnuchecked)
        self.ui.comboBox_nodeshape.currentIndexChanged.connect(self.setbtnuchecked)
        self.ui.comboBox_fontcor.currentIndexChanged.connect(self.setbtnuchecked)
        self.ui.comboBox_nodecor.currentIndexChanged.connect(self.setbtnuchecked)
        self.ui.lineEdit_nodesize.editingFinished.connect(self.setbtnuchecked)
        self.ui.lineEdit_vespeed.editingFinished.connect(self.setbtnuchecked)
        self.ui.pushButton_check.clicked.connect(self.check)
        # self.ui.pushButton_creatani.clicked.connect(lambda: print(form_inputs[self.mod].play_rate))

    def initUI(self, Qmodelidx):
        global filePath
        filePath = self.model01.filePath(Qmodelidx)
        hh = V_doConfig()

    def showgfmsg(self):
        index_node_type = 0
        index_node_label = 0
        text_nodesize = 60
        text_rate = 50
        index_node_color = 0
        index_font_color = 0
        if self.gfmsg.node_type == "Circle":
            index_node_type = 0
        elif self.gfmsg.node_type == "Square":
            index_node_type = 1

        if self.gfmsg.node_color == "000000":
            index_node_color = 0
        elif self.gfmsg.node_color == "#FF0000":
            index_node_color = 1
        elif self.gfmsg.node_color == "#008000":
            index_node_color = 2
        elif self.gfmsg.node_color == "#0000FF":
            index_node_color = 3

        if self.gfmsg.font_color == "000000":
            index_font_color = 0
        elif self.gfmsg.font_color == "#FF0000":
            index_font_color = 1
        elif self.gfmsg.font_color == "#008000":
            index_font_color = 2
        elif self.gfmsg.node_color == "#0000FF":
            index_font_color = 3

        text_rate = self.gfmsg.play_rate * 100
        text_nodesize = self.gfmsg.node_size * 100

        index_node_label = self.gfmsg.label
        self.ui.comboBox_nodeshape.setCurrentIndex(index_node_type)
        self.ui.comboBox_fontcor.setCurrentIndex(index_font_color)
        self.ui.comboBox_nodecor.setCurrentIndex(index_node_color)
        self.ui.lineEdit_nodesize.setText(str(text_nodesize))
        self.ui.lineEdit_vespeed.setText(str(text_rate))
        self.ui.comboBox_label.setCurrentIndex(index_node_label)

    def setbtnuchecked(self):
        self.ui.pushButton_check.setChecked(False)

    def check(self):
        if self.ui.pushButton_check.isChecked():
            self.set_gfmsg_label()
            self.set_gfmsg_fontcor()
            self.set_gfmsg_nodecor()
            self.set_gfmsg_vespeed()
            self.set_gfmsg_node_type()
            self.set_gfmsg_nodesize()

    def change_form_inputs(self):
        checked_id = self.btn_group.checkedId()
        index = self.ui.comboBox_yangshi.currentIndex()
        if checked_id == 2:
            if index == 0:
                form_inputs["Heap"] = GrokFormMsg_ArrHeap
            elif index == 1:
                form_inputs["Heap"] = GrokFormMsg_TreeHeap
        self.gfmsg = form_inputs[self.mod]
        self.showgfmsg()
        self.ui.pushButton_check.setChecked(False)

    def set_gfmsg_nodesize(self):
        index = float(self.ui.lineEdit_nodesize.text())
        self.gfmsg.set_size(index)

    def set_gfmsg_vespeed(self):
        index = float(self.ui.lineEdit_vespeed.text())
        self.gfmsg.set_rate(index)

    def set_gfmsg_node_type(self):
        index = self.ui.comboBox_nodeshape.currentIndex()
        if index == 0:
            self.gfmsg.change_node_type("Circle")
        elif index == 1:
            self.gfmsg.change_node_type("Square")

    def set_gfmsg_fontcor(self):
        index = self.ui.comboBox_fontcor.currentIndex()
        if index == 0:
            self.gfmsg.change_font_color("#000000")  # 黑
        elif index == 1:
            self.gfmsg.change_font_color("#FF0000")  # 红
        elif index == 2:
            self.gfmsg.change_font_color("#008000")  # 绿
        elif index == 3:
            self.gfmsg.change_font_color("#0000FF")  # 蓝

    def set_gfmsg_nodecor(self):
        index = self.ui.comboBox_nodecor.currentIndex()
        if index == 0:
            self.gfmsg.change_node_color("#000000")  # 黑
        elif index == 1:
            self.gfmsg.change_node_color("#FF0000")  # 红
        elif index == 2:
            self.gfmsg.change_node_color("#008000")  # 绿
        elif index == 3:
            self.gfmsg.change_node_color("#0000FF")  # 蓝

    def set_gfmsg_label(self):
        if self.ui.comboBox_label.currentIndex():
            self.gfmsg.label_on()
        else:
            self.gfmsg.label_off()

    def set_gfmsg(self):
        checked_id = self.btn_group.checkedId()
        # print(checked_id)
        if checked_id == 0:
            self.mod = "vector"
            self.ui.comboBox_yangshi.clear()
        elif checked_id == 3:
            self.mod = "Tree"
            self.ui.comboBox_yangshi.clear()
        elif checked_id == 2:
            self.mod = "Heap"
            self.ui.comboBox_yangshi.clear()
            self.ui.comboBox_yangshi.insertItem(0, "Arr")
            self.ui.comboBox_yangshi.insertItem(1, "Tree")
        elif checked_id == 1:
            self.mod = "stack"
            self.ui.comboBox_yangshi.clear()
        self.gfmsg = form_inputs[self.mod]
        self.showgfmsg()
        self.ui.pushButton_check.setChecked(False)

    def slotStart(self):
        image_file, _ = QFileDialog.getOpenFileName(self, "Open", "", "*.avi *.mp4;;All Files(*)")
        if image_file != "":  # “”为用户取消
            return image_file

    def on_pushButton_view_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)  # 动画浏览页面

    def on_pushButton_settings_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)  # 设置界面

    # 拖动和放缩
    def mousePressEvent(self, event):
        try:
            if self.childAt(event.x(), event.y()) in [self.ui.frame_6]:
                try:
                    self.evn = 1
                    self.mouse_x = event.globalX()  # 获取鼠标当前的坐标
                    self.mouse_y = event.globalY()
                    self.origin_x = self.x()  # 获取窗体当前坐标
                    self.origin_y = self.y()
                except BaseException as f:
                    pass
            elif self.childAt(event.x(), event.y()) in [self.ui.frame_2]:
                try:
                    self.evn = 2
                    self.mouse_x = event.globalX()  # 获取鼠标当前的坐标
                    self.mouse_y = event.globalY()
                    self.origin_x = self.x()  # 获取窗体当前坐标
                    self.origin_y = self.y()
                except BaseException as f:
                    pass
            elif self.childAt(event.x(), event.y()) in [self.ui.frame_3]:
                try:
                    self.evn = 3
                    self.mouse_x = event.globalX()  # 获取鼠标当前的坐标
                    self.mouse_y = event.globalY()
                    self.origin_x = self.x()  # 获取窗体当前坐标
                    self.origin_y = self.y()
                except BaseException as f:
                    pass
            elif self.childAt(event.x(), event.y()) in [self.ui.frame_top]:
                try:
                    self.evn = 0
                    super(MainWin, self).mousePressEvent(event)
                    self.start_x = event.x()
                    self.start_y = event.y()
                except BaseException as f:
                    pass
            else:
                self.evn = 4

        except BaseException as f:
            pass

    def mouseReleaseEvent(self, event):
        if self.evn != 4:
            try:
                self.origin_x = None
                self.origin_y = None
                self.start_x = None
                self.start_y = None
            except BaseException as f:
                pass

    def mouseMoveEvent(self, event):
        if self.evn == 0:
            super(MainWin, self).mouseMoveEvent(event)
            dis_x = event.x() - self.start_x
            dis_y = event.y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
        elif self.evn == 1:  # 计算鼠标移动的x，y位移
            try:
                if event.x() < 814:
                    x = 814
                else:
                    x = event.x()
                if event.y() < 272:
                    y = 272
                else:
                    y = event.y()
                self.setGeometry(self.origin_x, self.origin_y, x, y)
                self.ui.frame.setGeometry(0, 0, x, y)
            except BaseException as f:
                pass
        elif self.evn == 2:  # 计算鼠标移动的x，y位移
            try:
                # 移动窗体
                if event.x() < 814:
                    x = 814
                else:
                    x = event.x()
                self.setGeometry(self.origin_x, self.origin_y, x, self.height())
                self.ui.frame.setGeometry(0, 0, x, self.ui.frame.height())
            except BaseException as f:
                pass
        elif self.evn == 3:  # 计算鼠标移动的x，y位移
            try:
                # 移动窗体
                if event.y() < 272:
                    y = 272
                else:
                    y = event.y()
                self.setGeometry(self.origin_x, self.origin_y, self.width(), y)
                self.ui.frame.setGeometry(0, 0, self.ui.frame.width(), y)
            except BaseException as f:
                pass
        elif self.evn == 4:
            self.evn = 4

    # 最大化
    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.pushButton_max.setIcon(QtGui.QIcon(":/图标/24.全屏_最大化.png"))
        else:
            self.showMaximized()
            self.ui.pushButton_max.setIcon(QtGui.QIcon(":/图标/缩小.png"))


# 视频控制
class V_doConfig:
    def __init__(self):
        global filePath
        self.flag = True
        win.file = filePath
        self.v_timer = QTimer()
        self.cap = cv2.VideoCapture(filePath)
        if not self.cap:
            print("打开视频失败")
            return
        # 获取视频FPS
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)  # 获得码率
        # 获取视频总帧数
        self.total_f = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        # 获取视频当前帧所在的帧数
        self.current_f = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        # 设置定时器周期，单位毫秒
        self.v_timer.start(int(1000 / self.fps))
        print("FPS:".format(self.fps))
        win.ui.treeView.doubleClicked.connect(self.setflag)

        win.ui.pushButton_back.setEnabled(True)
        win.ui.pushButton_stop.setEnabled(True)
        win.ui.pushButton_forward.setEnabled(True)
        win.ui.horizontalSlider.setEnabled(True)
        win.ui.pushButton_stop.setIcon(QtGui.QIcon(":/图标/24gf-pause2.png"))

        # 连接定时器周期溢出的槽函数，用于显示一帧视频
        self.v_timer.timeout.connect(self.show_pic)
        # 连接按钮和对应槽函数，lambda表达式用于传参
        win.ui.pushButton_stop.clicked.connect(self.go_pause)
        win.ui.pushButton_back.pressed.connect(lambda: self.last_img(True))
        win.ui.pushButton_back.clicked.connect(lambda: self.last_img(False))
        win.ui.pushButton_forward.pressed.connect(lambda: self.next_img(True))
        win.ui.pushButton_forward.clicked.connect(lambda: self.next_img(False))
        win.ui.horizontalSlider.sliderMoved.connect(self.change_img)
        # win.ui.horizontalSlider.valueChanged.connect(self.change_img)
        print("init OK")

        # 视频播放
    def setflag(self):
        self.v_timer.stop()
        self.flag = False

    def show_pic(self):
        # 读取一帧
        if self.flag:
            success, frame = self.cap.read()
            if success:
                # Mat格式图像转Qt中图像的方法
                show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, bytesPerComponent = show.shape
                bytesPerLine = bytesPerComponent * width
                showImage = QImage(show.data, width, height, bytesPerLine,
                                   QImage.Format_RGB888)
                win.ui.label_2.setPixmap(QPixmap.fromImage(showImage))
                win.ui.label_2.setScaledContents(True)  # 让图片自适应 label 大小

                # 状态栏显示信息
                self.current_f = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                current_t, total_t = self.calculate_time(self.current_f, self.total_f, self.fps)
                win.ui.label.setText("{}({})".format(current_t, total_t))

                # 滑动条移动
                c_s = int(self.current_f / self.fps)
                t_s = int(self.total_f / self.fps)
                slidevalue = int(1000 * c_s / t_s)
                win.ui.horizontalSlider.setValue(slidevalue)

    def calculate_time(self, c_f, t_f, fps):
        total_seconds = int(t_f / fps)
        current_sec = int(c_f / fps)
        c_time = "{}:{}:{}".format(int(current_sec / 3600), int((current_sec % 3600) / 60), int(current_sec % 60))
        t_time = "{}:{}:{}".format(int(total_seconds / 3600), int((total_seconds % 3600) / 60), int(total_seconds % 60))
        return c_time, t_time

    def show_pic_back(self):
        if self.flag:
            # 获取视频当前帧所在的帧数
            self.current_f = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            # 设置下一次帧为当前帧-20
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_f - 20)
            # 读取一帧
            success, frame = self.cap.read()
            if success:
                show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, bytesPerComponent = show.shape
                bytesPerLine = bytesPerComponent * width
                showImage = QImage(show.data, width, height, bytesPerLine,
                                   QImage.Format_RGB888)
                win.ui.label_2.setPixmap(QPixmap.fromImage(showImage))

                # 状态栏显示信息
                current_t, total_t = self.calculate_time(self.current_f - 1, self.total_f, self.fps)
                win.ui.label.setText("{}({})".format(current_t, total_t))

                # 滑动条移动
                c_s = int(self.current_f / self.fps)
                t_s = int(self.total_f / self.fps)
                slidevalue = int(1000 * c_s / t_s)
                win.ui.horizontalSlider.setValue(slidevalue)

            # 快退

    def last_img(self, t):
        if self.flag:
            win.ui.pushButton_stop.setIcon(QtGui.QIcon(":/图标/24gf-pause2.png"))
            if t:
                # 断开槽连接
                self.v_timer.timeout.disconnect(self.show_pic)
                # 连接槽连接
                self.v_timer.timeout.connect(self.show_pic_back)
                self.v_timer.start(int(self.fps / 10))
            else:
                self.v_timer.timeout.disconnect(self.show_pic_back)
                self.v_timer.timeout.connect(self.show_pic)
                self.v_timer.start(int(1000 / self.fps))

            # 快进

    def next_img(self, t):
        if self.flag:
            win.ui.pushButton_stop.setIcon(QtGui.QIcon(":/图标/24gf-pause2.png"))
            if t:
                self.v_timer.start(int(50 / self.fps / 2))  # 快进
            else:

                self.v_timer.start(int(1000 / self.fps))

        # 暂停播放

    def go_pause(self):
        if self.flag:
            if self.v_timer.isActive():
                self.v_timer.stop()
                win.ui.pushButton_stop.setIcon(QtGui.QIcon(":/图标/开始1.png"))
            else:
                self.v_timer.start(int(1000 / self.fps))
                win.ui.pushButton_stop.setIcon(QtGui.QIcon(":/图标/24gf-pause2.png"))

        # 进度条控制

    def change_img(self):
        if self.flag:
            self.v_timer.timeout.disconnect(self.show_pic)
            self.current_f = int(win.ui.horizontalSlider.value() / 1000 * self.total_f)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_f)
            # 读取一帧
            success, frame = self.cap.read()
            if success:
                show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, bytesPerComponent = show.shape
                bytesPerLine = bytesPerComponent * width
                showImage = QImage(show.data, width, height, bytesPerLine,
                                   QImage.Format_RGB888)
                win.ui.label_2.setPixmap(QPixmap.fromImage(showImage))

                # 状态栏显示信息
                current_t, total_t = self.calculate_time(self.current_f - 1, self.total_f, self.fps)
                win.ui.label.setText("{}({})".format(current_t, total_t))

            self.v_timer.timeout.connect(self.show_pic)
            self.v_timer.start(int(1000 / self.fps))


class grokMsgList:
    def __init__(self, _init_msg_: str):
        _rets = _init_msg_.split(' ', 3)
        self.mob_type = _rets[2]
        self.Animque = list()
        if _rets.__len__() > 3:
            self.Animque.append(_rets[0] + ' ' + _rets[1] + ' ' + _rets[3])
        else:
            self.Animque.append(_rets[0] + ' ' + _rets[1])

    def push(self, _msg_: str):
        self.Animque.append(_msg_)
        return int(_msg_.split(' ', 1)[0])

    def write(self):
        fo = open(_path, 'w')
        for cur in self.Animque:
            fo.write(cur + '\n')
        fo.close()
        return self.mob_type


class grokUdpServer:
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.local_addr = ("127.0.0.1", 7851)
        self.udp_socket.bind(self.local_addr)

    def listen(self):
        Thread(target=self.receive).start()

    def receive(self):
        while 1:
            ret = self.udp_socket.recvfrom(1024)
            _pro_id = ret[1][1]
            temp = ret[0].decode('utf-8').split(' ', 1)
            _g_id = int(temp[0])
            __msg_ = temp[1]

            if grok_inputs.get(_pro_id) is None:
                grok_inputs[_pro_id] = dict()
            if grok_inputs[_pro_id].get(_g_id) is None:
                grok_inputs[_pro_id][_g_id] = grokMsgList(__msg_)
            else:
                if grok_inputs[_pro_id][_g_id].push(__msg_) == -1:
                    ss = grok_inputs[_pro_id][_g_id].write()
                    comline = "manim -pqh datastruct/" + mob_to_manim[ss] + " object"
                    os.system(comline)
                    grok_inputs[_pro_id].pop(_g_id)


grok_inputs = dict()

form_inputs = {
    "vector": GrokFormMsg_vector,
    "Heap": GrokFormMsg_ArrHeap,
    "stack": GrokFormMsg_stack,
    "Tree": GrokFormMsg_Tree
}

mob_to_manim = {
    "vector": "visual_arr.py",
    "Heap": "visual_tarray_heap.py",
    "stack": "visual_stack.py",
    "queue": "visual_queue_fade.py"
}

filePath = ''

_path = "grok_to_manim"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    grok_udp = grokUdpServer()
    grok_udp.listen()
    win = MainWin()
    win.show()
    sys.exit(app.exec_())
