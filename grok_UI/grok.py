import shutil

import cv2

from final_ui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QButtonGroup, QAbstractButton, QFileSystemModel
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, Qt
import sys
import socket
import os
filePath = ' '
_path = "../grok_to_manim"
grok_inputs = dict()

saved = {}
save_filePath = ''
class GrokFormMsg:
    def __init__(self, mob, node_type="Circle", font_color="#00FFFF", node_color="#FF7AB2",
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

    def to_string(self):
        return '0 0 ' + self.node_type + ' ' + self.font_color +  ' ' + self.node_color  + ' ' + \
        str(self.label) + ' ' + str(self.node_size) + ' '  + str(self.play_rate)
# mob_to_manim = {
#     "vector": "visual_arr",          #数组
#     "Heap": "visual_tarray_heap",    #堆
#     "stack": "visual_stack",         #栈
#     "queue": "visual_queue",         #队列
#     "unionfindset": "visual_unionfindset",#并查集
#     "SegmentTree": "visual_segmenttree",#线段树
#     "scapegoat": "visual_scapegoat", #替罪羊树
#     "Bst": "visual_bst", #二叉搜索树
#     "rbt": "visual_rbt"  #红黑树
# }
GrokFormMsg_Arr_vector = GrokFormMsg("visual_arr")
GrokFormMsg_Tree_vector = GrokFormMsg("visual_tarray")
GrokFormMsg_TreeHeap = GrokFormMsg("visual_tarray_heap")
GrokFormMsg_ArrHeap = GrokFormMsg("visual_arr_heap")
GrokFormMsg_stack_row = GrokFormMsg("visual_stack_fade")
GrokFormMsg_stack_col = GrokFormMsg("visual_stack")
GrokFormMsg_queue = GrokFormMsg("visual_queue")
GrokFormMsg_unionfindset = GrokFormMsg("visual_unionfindset")
GrokFormMsg_SegmentTree = GrokFormMsg("visual_segmenttree")
GrokFormMsg_Bst = GrokFormMsg("visual_bst")
GrokFormMsg_rbt = GrokFormMsg("visual_rbt")
GrokFormMsg_scapegoat = GrokFormMsg("visual_scapegoat")

form_inputs = {
    "vector": GrokFormMsg_Arr_vector, # 数组
    "Heap": GrokFormMsg_ArrHeap, # 堆
    "stack": GrokFormMsg_stack_col, # 栈
    "queue": GrokFormMsg_queue, # 队列
    "unionfindset": GrokFormMsg_unionfindset,# 并查集
    "SegmentTree":GrokFormMsg_SegmentTree, # 线段树
    "Bst" :GrokFormMsg_Bst ,# 二叉搜索树
    "rbt": GrokFormMsg_rbt,# 红黑树
    "scapegoat": GrokFormMsg_scapegoat# 替罪羊树
}

path_dist = {}

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

    def push_front(self, _msg_):
        self.Animque.insert(0, _msg_)
        return int(_msg_.split(' ', 1)[0])

    def write(self):
        fo = open(_path, 'w')
        for cur in self.Animque:
            fo.write(cur + '\n')
        fo.close()
        return self.mob_type
class grokUdpServer(QtCore.QThread):
    new_object = QtCore.pyqtSignal(str)
    quality = 0

    def __init__(self):

        super().__init__()
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.local_addr = ("127.0.0.1", 7851)
        self.udp_socket.bind(self.local_addr)

    def listen(self):
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
                grok_inputs[_pro_id][_g_id].push_front(
                    form_inputs[grok_inputs[_pro_id][_g_id].mob_type].to_string()
                )
            else:
                if grok_inputs[_pro_id][_g_id].push(__msg_) == -1:
                    filename = str(_pro_id) + '_' + str(_g_id)
                    ss = grok_inputs[_pro_id][_g_id].write()
                    video_path = 'media/videos/'+ form_inputs[ss].mob +'/'
                    level = ''
                    if self.quality == 1:
                        video_path += '720p30/' + filename + '.mp4'
                        level = 'm'
                    elif self.quality == 0:
                        video_path += '1080p60/' + filename + '.mp4'
                        level = 'h'
                    elif self.quality == 2:
                        video_path += '480p15/' + filename + '.mp4'
                        level = 'l'

                    sendstr = str(_pro_id) + ' ' + str(_g_id) + ' ' + ss + ' ' + video_path
                    self.new_object.emit(sendstr)

                    comline = "manim -q" + level +\
                              " ../datastruct/" + form_inputs[ss].mob + ".py -o " + filename
                    os.system(comline)
                    saved[video_path] = False
                    grok_inputs[_pro_id].pop(_g_id)


    def run(self):
        self.listen()




class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.verticalLayout = None
        # self.pushButton_vdo = None
        # self.page = None
        # self.pushButton_pro = None
        self.btn_group_top = QButtonGroup(self)
        self.btn_group_top.buttonClicked[QAbstractButton].connect(self.set_vdopage)
        self.mod = "vector"
        self.gfmsg = GrokFormMsg_Arr_vector
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
        self.model01.setRootPath(" ")
        self.model01.setNameFilterDisables(False)  # 过滤掉的灰色文件不显示
        self.model01.setNameFilters(['*.mp4'])
        # self.ui.treeView.setModel(self.model01)
        # for col in range(1, 4):
        #     self.ui.treeView.setColumnHidden(col, True)
        # self.ui.treeView.doubleClicked.connect(self.initUI)
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
        self.btn_group.addButton(self.ui.pushButton_stack, 2)
        self.btn_group.addButton(self.ui.pushButton_heap, 1)
        self.btn_group.addButton(self.ui.pushButton_queue, 3)
        self.btn_group.buttonClicked[QAbstractButton].connect(self.set_gfmsg)
        self.ui.comboBox_yangshi.currentIndexChanged.connect(self.change_form_inputs)
        self.ui.comboBox_label.currentIndexChanged.connect(self.setbtnuchecked)
        self.ui.comboBox_nodeshape.currentIndexChanged.connect(self.setbtnuchecked)
        self.ui.comboBox_fontcor.currentIndexChanged.connect(self.setbtnuchecked)
        self.ui.comboBox_nodecor.currentIndexChanged.connect(self.setbtnuchecked)
        self.ui.lineEdit_nodesize.editingFinished.connect(self.setbtnuchecked)
        self.ui.lineEdit_vespeed.editingFinished.connect(self.setbtnuchecked)
        self.ui.pushButton_check.clicked.connect(self.check)
        self.ui.pushButtonFile.clicked.connect(self.set_filepath)
        self.ui.verticalLayout_9.setAlignment(QtCore.Qt.AlignTop)
#        self.ui.horizontalLayout.setAlignment(QtCore.Qt.AlignLeft)

        # 按钮信号模拟发送来的信号
        # self.ui.pushButton_3.clicked.connect(self.add_pro)
        self.udp = grokUdpServer()
        self.udp.new_object.connect(self.handleDisplay)
        self.udp.start()
        self.procMap = {}
        # self.ui.pushButton_creatani.clicked.connect(lambda: print(form_inputs[self.mod].play_rate))

        self.ui.pushButton_check.setChecked(True)
        self.btn_group.addButton(self.ui.pushButton_ercs, 4)
        self.btn_group.addButton(self.ui.pushButton_honghei, 5)
        self.btn_group.addButton(self.ui.pushButton_tizuiy, 6)
        self.btn_group.addButton(self.ui.pushButton_bcj, 7)
        self.btn_group.addButton(self.ui.pushButton_xds, 8)
        self.ui.comboBox_yangshi.clear()
        self.ui.comboBox_yangshi.insertItem(0, "数组")
        self.ui.comboBox_yangshi.insertItem(1, "树形")
        self.ui.comboBox_yangshi.setCurrentIndex(0)

        self.ui.comboBox_nodeshape_2.currentIndexChanged.connect(self.setquality)

    def setquality(self, index):
        self.udp.quality = index

    def check(self):
        if self.ui.pushButton_check.isChecked():
            self.set_gfmsg_label()
            self.set_gfmsg_fontcor()
            self.set_gfmsg_nodecor()
            self.set_gfmsg_vespeed()
            self.set_gfmsg_node_type()
            self.set_gfmsg_nodesize()

    def handleDisplay(self, data):
        print('in')
        self.add_pro(data)

    def initUI(self, Qmodelidx):
        global filePath
        filePath = self.model01.filePath(Qmodelidx)
        hh = V_doConfig()

    def showgfmsg(self):
        index_node_type = 0
        index_node_label = 0
        text_nodesize = 60
        text_rate = 50
        index_fcolor = 0
        index_ncolor = 0
        if self.gfmsg.node_type == "Circle":
            index_node_type = 0
        elif self.gfmsg.node_type == "Square":
            index_node_type = 1
        elif self.gfmsg.node_type == "Num":
            index_node_type = 2
        elif self.gfmsg.node_type == "RoundedSquare":
            index_node_type = 3

        # print("节点颜色"+self.gfmsg.node_color)
        if self.gfmsg.font_color == "#00FEFE":
            index_fcolor = 0
        elif self.gfmsg.font_color == "#3F3FFF":
            index_fcolor = 1
        elif self.gfmsg.font_color == "#FF3F3F":
            index_fcolor = 2
        elif self.gfmsg.font_color == "#3FFF3F":
            index_fcolor = 3
        elif self.gfmsg.font_color == "#FF2AB2":
            index_fcolor = 4
        elif self.gfmsg.font_color == "#FF862F":
            index_fcolor = 5
        elif self.gfmsg.font_color == "#FEFE00":
            index_fcolor = 6
        elif self.gfmsg.font_color == "#FE00FE":
            index_fcolor = 7
        elif self.gfmsg.font_color == "#FEFEFE":
            index_fcolor = 8

        if self.gfmsg.node_color == "#FF862F":
            index_ncolor = 0
        elif self.gfmsg.node_color == "#FF3F3F":
            index_ncolor = 1
        elif self.gfmsg.node_color == "#3FFF3F":
            index_ncolor = 2
        elif self.gfmsg.node_color == "#FF2AB2":
            index_ncolor = 3
        elif self.gfmsg.node_color == "#3F3FFF":
            index_ncolor = 4
        elif self.gfmsg.node_color == "#FEFE00":
            index_ncolor = 5
        elif self.gfmsg.node_color == "#FE00FE":
            index_ncolor = 6
        elif self.gfmsg.node_color == "#00FEFE":
            index_ncolor = 7

        text_rate = self.gfmsg.play_rate * 100
        text_nodesize = self.gfmsg.node_size * 100

        index_node_label = self.gfmsg.label
        self.ui.comboBox_nodeshape.setCurrentIndex(index_node_type)
        self.ui.comboBox_fontcor.setCurrentIndex(index_fcolor)
        self.ui.comboBox_nodecor.setCurrentIndex(index_ncolor)
        self.ui.lineEdit_nodesize.setText(str(text_nodesize))
        self.ui.lineEdit_vespeed.setText(str(text_rate))
        self.ui.comboBox_label.setCurrentIndex(index_node_label)

    def setbtnuchecked(self):
        self.ui.pushButton_check.setChecked(False)

    def change_form_inputs(self):
        checked_id = self.btn_group.checkedId()
        index = self.ui.comboBox_yangshi.currentIndex()
        if checked_id == 1:
            if index == 0:
                form_inputs["Heap"] = GrokFormMsg_ArrHeap
            elif index == 1:
                form_inputs["Heap"] = GrokFormMsg_TreeHeap
            print(form_inputs["Heap"].mob)
        elif checked_id == 0:
            if index == 0:
                form_inputs["vector"] = GrokFormMsg_Arr_vector
            elif index == 1:
                form_inputs["vector"] = GrokFormMsg_Tree_vector
            print(form_inputs["vector"].mob)
        elif checked_id == 2:
            if index == 0:
                form_inputs["stack"] = GrokFormMsg_stack_col
            elif index == 1:
                form_inputs["stack"] = GrokFormMsg_stack_row
            print(form_inputs["stack"].mob)
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
        elif index == 2:
            self.gfmsg.change_node_type("Num") # 无边框
        elif index == 3:
            self.gfmsg.change_node_type("RoundedSquare") # 圆角方形

    def set_gfmsg_fontcor(self):
        index = self.ui.comboBox_fontcor.currentIndex()

        if index == 0:
            self.gfmsg.change_font_color("#00FEFE")  # 青
        elif index == 1:
            self.gfmsg.change_font_color("#3F3FFF")  # 蓝
        elif index == 2:
            self.gfmsg.change_font_color("#FF3F3F")  # 红
        elif index == 3:
            self.gfmsg.change_font_color("#3FFF3F")  # 绿
        elif index == 4:
            self.gfmsg.change_font_color("#FF7AB2")  # 粉
        elif index == 5:
            self.gfmsg.change_font_color("#FF862F")  # 橙
        elif index == 6:
            self.gfmsg.change_font_color("#FEFE00")  # 黄
        elif index == 7:
            self.gfmsg.change_font_color("#FE00FE")  # 紫
        elif index == 8:
            self.gfmsg.change_font_color("#FEFEFE")  # 白


    def set_gfmsg_nodecor(self):
        index = self.ui.comboBox_nodecor.currentIndex()
        if index == 0:
            self.gfmsg.change_node_color("#FF7AB2")  # 粉
        elif index == 1:
            self.gfmsg.change_node_color("#FF3F3F")  # 红
        elif index == 2:
            self.gfmsg.change_node_color("#3FFF3F")  # 绿
        elif index == 3:
            self.gfmsg.change_node_color("#3F3FFF")  # 蓝
        elif index == 4:
            self.gfmsg.change_node_color("#FF862F")  # 橙
        elif index == 5:
            self.gfmsg.change_node_color("#FEFE00")  # 黄
        elif index == 6:
            self.gfmsg.change_node_color("#FE00FE")  # 紫
        elif index == 7:
            self.gfmsg.change_node_color("#00FEFE")  # 青

    def set_gfmsg_label(self):
        if self.ui.comboBox_label.currentIndex():
            self.gfmsg.label_on()
        else:
            self.gfmsg.label_off()

    def set_gfmsg(self):
        checked_id = self.btn_group.checkedId()
        if checked_id == 0:
            self.mod = "vector"
            self.ui.comboBox_yangshi.clear()
            self.ui.comboBox_yangshi.insertItem(0, "数组")
            self.ui.comboBox_yangshi.insertItem(1, "树形")
        elif checked_id == 1:
            self.mod = "Heap"
            self.ui.comboBox_yangshi.clear()
            self.ui.comboBox_yangshi.insertItem(0, "数组")
            self.ui.comboBox_yangshi.insertItem(1, "树形")
        elif checked_id == 2:
            self.mod = "stack"
            self.ui.comboBox_yangshi.clear()
            self.ui.comboBox_yangshi.insertItem(0, "竖版")
            self.ui.comboBox_yangshi.insertItem(1, "横版")
        elif checked_id == 3:
            self.mod = "queue"
            self.ui.comboBox_yangshi.clear()
        elif checked_id == 4:
            self.mod = "Bst"
            self.ui.comboBox_yangshi.clear()
        elif checked_id == 5:
            self.mod = "rbt"
            self.ui.comboBox_yangshi.clear()
        elif checked_id == 6:
            self.mod = "scapegoat"
            self.ui.comboBox_yangshi.clear()
        elif checked_id == 7:
            self.mod = "unionfindset"
            self.ui.comboBox_yangshi.clear()
        elif checked_id == 8:
            self.mod = "SegmentTree"
            self.ui.comboBox_yangshi.clear()

        self.gfmsg = form_inputs[self.mod]
        self.showgfmsg()
        self.ui.pushButton_check.setChecked(False)

    def slot_start(self):
        image_file, _ = QFileDialog.getOpenFileName(self, "Open", "", "*.avi *.mp4;;All Files(*)")
        if image_file != "":  # “”为用户取消
            return image_file

    # 设置filePath全局变量
    def set_filepath(self):
        global save_filePath
        save_filePath = QFileDialog.getExistingDirectory(self, "选择保存的文件夹", "")
        self.ui.fileTextBrowser.setText(save_filePath)

    # def addTopPushButton(self):


    def add_pro(self, data):
        datas = str.split(data)
        pro_id = datas[0]
        g_id = datas[1]
        video_name = datas[2]
        video_path = datas[3]
        print(video_path)
        if self.procMap.get(pro_id) is None:
            self.procMap[pro_id] = PageConfig(pro_id, self.procMap.__len__())

        self.procMap[pro_id].add_vdo_btn(g_id, video_name, video_path)



    # 头部按钮跳转页面
    def set_vdopage(self):
        check_id = self.btn_group_top.checkedId()
        self.ui.stackedWidget_2.setCurrentIndex(check_id)

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
            elif self.childAt(event.x(), event.y()) in [self.ui.frame_choice]:
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
            dis_x = event.x() - (self.start_x if self.start_x is not None else 0)
            dis_y = event.y() - (self.start_y if self.start_y is not None else 0)
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
        # print(filePath)
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
        # win.ui.treeView.doubleClicked.connect(self.setflag)

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
                win.ui.label_2.setPixmap(QPixmap.fromImage(showImage).scaled(win.ui.label_2.width()
                                        ,win.ui.label_2.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation))

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
                win.ui.label_2.setPixmap(QPixmap.fromImage(showImage).scaled(win.ui.label_2.width()
                                                                             , win.ui.label_2.height(),
                                                                             Qt.KeepAspectRatio,
                                                                             Qt.SmoothTransformation))

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
            win.ui.pushButton_stop.setIcon(QtGui.QIcon(":/图标/24gf-pause2.png"))
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
                win.ui.label_2.setPixmap(QPixmap.fromImage(showImage).scaled(win.ui.label_2.width()
                                                                             , win.ui.label_2.height(),
                                                                             Qt.KeepAspectRatio,
                                                                             Qt.SmoothTransformation))

                # 状态栏显示信息
                current_t, total_t = self.calculate_time(self.current_f - 1, self.total_f, self.fps)
                win.ui.label.setText("{}({})".format(current_t, total_t))

            self.v_timer.timeout.connect(self.show_pic)
            self.v_timer.start(int(1000 / self.fps))

class PageConfig:
    def __init__(self, pro_id, pushbutton_val):
        # 上面的按钮
        self.pushButton_pro = QtWidgets.QPushButton(win.ui.frame_4)
        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(self.pushButton_pro.sizePolicy().hasHeightForWidth())
        self.pushButton_pro.setSizePolicy(self.sizePolicy)
        self.pushButton_pro.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_pro.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pushButton_pro.setCheckable(True)
        self.pushButton_pro.setObjectName("pushButton" + str(pushbutton_val))
        # 设置按钮名字，可以根据self.name来设
        self.pushButton_pro.setText('项目' + str(pushbutton_val))
        # 加入按钮组
        win.btn_group_top.addButton(self.pushButton_pro, pushbutton_val)

        # pushbutton_val += 1
        # 头部按钮加入到UI界面
        win.ui.horizontalLayout.addWidget(self.pushButton_pro)

        # 增加页面
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page" + str(pro_id))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout.setObjectName("verticalLayout" + str(pro_id))

        # 视频按钮组（竖着的按钮们）
        self.btn_group_vdo = QButtonGroup()
        self.btn_group_vdo.buttonClicked[QAbstractButton].connect(self.play_vdo)
        self.namelist = dict()
        self.name = pro_id
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)

        win.ui.stackedWidget_2.addWidget(self.page)

    def add_vdo_btn(self, video_id, video_name, video_path):
        if self.namelist.get(video_name) is None:
            self.namelist[video_name] = 0
        else:
            self.namelist[video_name] += 1
            video_name += '_' + str(self.namelist[video_name])

        pushButton_vdo = QtWidgets.QPushButton(self.page)
        pushButton_vdo.setObjectName("pushButtonVdo" + video_id)
        # 视频名字，可以根据data来设置
        pushButton_vdo.setText(video_name)
        pushButton_vdo.setCheckable(True)

        self.verticalLayout.addWidget(pushButton_vdo)
        # 加入视频播放按钮组
        self.btn_group_vdo.addButton(pushButton_vdo, -1)

        # 视频的地址
        path_dist[pushButton_vdo] = video_path

    def play_vdo(self, btn):
        global filePath
        if not os.path.exists(path_dist[btn]):
            filePath = 'Koch.mp4'
            for m in vdolist:
                m.setflag()
            vdolist.append(V_doConfig())
        else:
            filePath = path_dist[btn]
            if save_filePath.__len__() > 0 and saved[filePath] == False:
                source = filePath
                target = save_filePath
                shutil.copy(source, target)
                saved[filePath] = True

            for m in vdolist:
                m.setflag()
            vdolist.append(V_doConfig())



vdolist = []



path_dist = { }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())
