# -*- coding: utf-8 -*-
import sys

################################################################################
## Form generated from reading UI file 'MainWindow_SummaryPage_6tfWDlu.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QListView,
    QMainWindow, QMenuBar, QProgressBar, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 683)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1024, 0))
        MainWindow.setMaximumSize(QSize(1024, 16777215))
        icon = QIcon()
        iconThemeName = u"media-tape"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u"C:/Users/brenn/.designer/backup", QSize(), QIcon.Normal, QIcon.Off)

        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMinimumSize(QSize(1024, 610))
        self.centralwidget.setMaximumSize(QSize(1024, 16777215))
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_videoSelection = QHBoxLayout()
        self.horizontalLayout_videoSelection.setObjectName(u"horizontalLayout_videoSelection")
        self.label_videoSelection_description = QLabel(self.centralwidget)
        self.label_videoSelection_description.setObjectName(u"label_videoSelection_description")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_videoSelection_description.sizePolicy().hasHeightForWidth())
        self.label_videoSelection_description.setSizePolicy(sizePolicy2)
        self.label_videoSelection_description.setMinimumSize(QSize(50, 0))
        font = QFont()
        font.setBold(True)
        self.label_videoSelection_description.setFont(font)

        self.horizontalLayout_videoSelection.addWidget(self.label_videoSelection_description)

        self.comboBox_videoSelection_box = QComboBox(self.centralwidget)
        self.comboBox_videoSelection_box.setObjectName(u"comboBox_videoSelection_box")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBox_videoSelection_box.sizePolicy().hasHeightForWidth())
        self.comboBox_videoSelection_box.setSizePolicy(sizePolicy3)
        self.comboBox_videoSelection_box.setMinimumSize(QSize(300, 0))
        self.comboBox_videoSelection_box.setPlaceholderText("(select or add video)")

        self.horizontalLayout_videoSelection.addWidget(self.comboBox_videoSelection_box)

        self.pushButton_videoSelection_add = QPushButton(self.centralwidget)
        self.pushButton_videoSelection_add.setObjectName(u"pushButton_videoSelection_add")
        sizePolicy3.setHeightForWidth(self.pushButton_videoSelection_add.sizePolicy().hasHeightForWidth())
        self.pushButton_videoSelection_add.setSizePolicy(sizePolicy3)
        self.pushButton_videoSelection_add.setMinimumSize(QSize(25, 0))

        self.horizontalLayout_videoSelection.addWidget(self.pushButton_videoSelection_add)

        self.pushButton_videoSelection_openFolder = QPushButton(self.centralwidget)
        self.pushButton_videoSelection_openFolder.setObjectName(u"pushButton_videoSelection_openFolder")

        self.horizontalLayout_videoSelection.addWidget(self.pushButton_videoSelection_openFolder)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_videoSelection.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_videoSelection)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_presetSelection_description = QLabel(self.centralwidget)
        self.label_presetSelection_description.setObjectName(u"label_presetSelection_description")
        sizePolicy2.setHeightForWidth(self.label_presetSelection_description.sizePolicy().hasHeightForWidth())
        self.label_presetSelection_description.setSizePolicy(sizePolicy2)
        self.label_presetSelection_description.setMinimumSize(QSize(50, 0))
        self.label_presetSelection_description.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_presetSelection_description)

        self.comboBox_presetSelection_box = QComboBox(self.centralwidget)
        self.comboBox_presetSelection_box.setObjectName(u"comboBox_presetSelection_box")
        sizePolicy3.setHeightForWidth(self.comboBox_presetSelection_box.sizePolicy().hasHeightForWidth())
        self.comboBox_presetSelection_box.setSizePolicy(sizePolicy3)
        self.comboBox_presetSelection_box.setMinimumSize(QSize(300, 0))
        self.comboBox_presetSelection_box.setPlaceholderText("(select preset option)")

        self.horizontalLayout_2.addWidget(self.comboBox_presetSelection_box)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tabWidget_content = QTabWidget(self.centralwidget)
        self.tabWidget_content.setObjectName(u"tabWidget_content")
        self.tabWidget_content.setMaximumSize(QSize(16777215, 500))
        self.tabWidget_content.setTabEnabled(1,False) #Disable Details Tab at startup
        font1 = QFont()
        font1.setBold(False)
        self.tabWidget_content.setFont(font1)
        self.tab_summary = QWidget()
        self.tab_summary.setObjectName(u"tab_summary")
        self.gridLayout = QGridLayout(self.tab_summary)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_tab_summary = QHBoxLayout()
        self.horizontalLayout_tab_summary.setObjectName(u"horizontalLayout_tab_summary")
        self.verticalLayout_summary = QVBoxLayout()
        self.verticalLayout_summary.setObjectName(u"verticalLayout_summary")
        self.horizontalLayout_videoFileType = QHBoxLayout()
        self.horizontalLayout_videoFileType.setObjectName(u"horizontalLayout_videoFileType")
        self.label_summary_format_description = QLabel(self.tab_summary)
        self.label_summary_format_description.setObjectName(u"label_summary_format_description")
        sizePolicy3.setHeightForWidth(self.label_summary_format_description.sizePolicy().hasHeightForWidth())
        self.label_summary_format_description.setSizePolicy(sizePolicy3)
        self.label_summary_format_description.setMinimumSize(QSize(160, 0))
        self.label_summary_format_description.setFont(font)

        self.horizontalLayout_videoFileType.addWidget(self.label_summary_format_description)

        self.label_summary_format_content = QLabel(self.tab_summary)
        self.label_summary_format_content.setObjectName(u"label_summary_format_content")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_summary_format_content.sizePolicy().hasHeightForWidth())
        self.label_summary_format_content.setSizePolicy(sizePolicy4)

        self.horizontalLayout_videoFileType.addWidget(self.label_summary_format_content)


        self.verticalLayout_summary.addLayout(self.horizontalLayout_videoFileType)

        self.verticalSpacer_4 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_summary.addItem(self.verticalSpacer_4)

        self.horizontalLayout_resolutionSize = QHBoxLayout()
        self.horizontalLayout_resolutionSize.setObjectName(u"horizontalLayout_resolutionSize")
        self.label_summary_resolution_description = QLabel(self.tab_summary)
        self.label_summary_resolution_description.setObjectName(u"label_summary_resolution_description")
        sizePolicy3.setHeightForWidth(self.label_summary_resolution_description.sizePolicy().hasHeightForWidth())
        self.label_summary_resolution_description.setSizePolicy(sizePolicy3)
        self.label_summary_resolution_description.setMinimumSize(QSize(160, 0))
        self.label_summary_resolution_description.setFont(font)

        self.horizontalLayout_resolutionSize.addWidget(self.label_summary_resolution_description)

        self.label_summary_resolution_content = QLabel(self.tab_summary)
        self.label_summary_resolution_content.setObjectName(u"label_summary_resolution_content")
        sizePolicy4.setHeightForWidth(self.label_summary_resolution_content.sizePolicy().hasHeightForWidth())
        self.label_summary_resolution_content.setSizePolicy(sizePolicy4)

        self.horizontalLayout_resolutionSize.addWidget(self.label_summary_resolution_content)


        self.verticalLayout_summary.addLayout(self.horizontalLayout_resolutionSize)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_summary.addItem(self.verticalSpacer_5)

        self.horizontalLayout_duration = QHBoxLayout()
        self.horizontalLayout_duration.setObjectName(u"horizontalLayout_duration")
        self.label_summary_duration_description = QLabel(self.tab_summary)
        self.label_summary_duration_description.setObjectName(u"label_summary_duration_description")
        sizePolicy3.setHeightForWidth(self.label_summary_duration_description.sizePolicy().hasHeightForWidth())
        self.label_summary_duration_description.setSizePolicy(sizePolicy3)
        self.label_summary_duration_description.setMinimumSize(QSize(160, 0))
        self.label_summary_duration_description.setFont(font)

        self.horizontalLayout_duration.addWidget(self.label_summary_duration_description)

        self.label_summary_duration_content = QLabel(self.tab_summary)
        self.label_summary_duration_content.setObjectName(u"label_summary_duration_content")
        sizePolicy4.setHeightForWidth(self.label_summary_duration_content.sizePolicy().hasHeightForWidth())
        self.label_summary_duration_content.setSizePolicy(sizePolicy4)

        self.horizontalLayout_duration.addWidget(self.label_summary_duration_content)


        self.verticalLayout_summary.addLayout(self.horizontalLayout_duration)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_summary.addItem(self.verticalSpacer_3)

        self.horizontalLayout_frameRate = QHBoxLayout()
        self.horizontalLayout_frameRate.setObjectName(u"horizontalLayout_frameRate")
        self.label_summary_framerate_description = QLabel(self.tab_summary)
        self.label_summary_framerate_description.setObjectName(u"label_summary_framerate_description")
        sizePolicy3.setHeightForWidth(self.label_summary_framerate_description.sizePolicy().hasHeightForWidth())
        self.label_summary_framerate_description.setSizePolicy(sizePolicy3)
        self.label_summary_framerate_description.setMinimumSize(QSize(160, 0))
        self.label_summary_framerate_description.setFont(font)

        self.horizontalLayout_frameRate.addWidget(self.label_summary_framerate_description)

        self.label_summary_framerate_content = QLabel(self.tab_summary)
        self.label_summary_framerate_content.setObjectName(u"label_summary_framerate_content")
        sizePolicy4.setHeightForWidth(self.label_summary_framerate_content.sizePolicy().hasHeightForWidth())
        self.label_summary_framerate_content.setSizePolicy(sizePolicy4)

        self.horizontalLayout_frameRate.addWidget(self.label_summary_framerate_content)


        self.verticalLayout_summary.addLayout(self.horizontalLayout_frameRate)

        self.verticalSpacer_6 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_summary.addItem(self.verticalSpacer_6)

        self.horizontalLayout_summary_frames = QHBoxLayout()
        self.horizontalLayout_summary_frames.setObjectName(u"horizontalLayout_summary_frames")
        self.label_summary_frames_description = QLabel(self.tab_summary)
        self.label_summary_frames_description.setObjectName(u"label_summary_frames_description")
        sizePolicy3.setHeightForWidth(self.label_summary_frames_description.sizePolicy().hasHeightForWidth())
        self.label_summary_frames_description.setSizePolicy(sizePolicy3)
        self.label_summary_frames_description.setMinimumSize(QSize(160, 0))
        self.label_summary_frames_description.setFont(font)

        self.horizontalLayout_summary_frames.addWidget(self.label_summary_frames_description)

        self.label_summary_frames_content = QLabel(self.tab_summary)
        self.label_summary_frames_content.setObjectName(u"label_summary_frames_content")
        sizePolicy4.setHeightForWidth(self.label_summary_frames_content.sizePolicy().hasHeightForWidth())
        self.label_summary_frames_content.setSizePolicy(sizePolicy4)

        self.horizontalLayout_summary_frames.addWidget(self.label_summary_frames_content)


        self.verticalLayout_summary.addLayout(self.horizontalLayout_summary_frames)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_summary.addItem(self.verticalSpacer_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_summary_processed_Description = QLabel(self.tab_summary)
        self.label_summary_processed_Description.setObjectName(u"label_summary_processed_Description")
        sizePolicy3.setHeightForWidth(self.label_summary_processed_Description.sizePolicy().hasHeightForWidth())
        self.label_summary_processed_Description.setSizePolicy(sizePolicy3)
        self.label_summary_processed_Description.setMinimumSize(QSize(160, 0))
        self.label_summary_processed_Description.setFont(font)

        self.horizontalLayout_6.addWidget(self.label_summary_processed_Description)

        self.label_summary_processed_content = QLabel(self.tab_summary)
        self.label_summary_processed_content.setObjectName(u"label_summary_processed_content")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_summary_processed_content.sizePolicy().hasHeightForWidth())
        self.label_summary_processed_content.setSizePolicy(sizePolicy5)

        self.horizontalLayout_6.addWidget(self.label_summary_processed_content)


        self.verticalLayout_summary.addLayout(self.horizontalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 300, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_summary.addItem(self.verticalSpacer)

        self.horizontalLayout_processButton = QHBoxLayout()
        self.horizontalLayout_processButton.setObjectName(u"horizontalLayout_processButton")
        self.pushButton_summary_process = QPushButton(self.tab_summary)
        self.pushButton_summary_process.setObjectName(u"pushButton_summary_process")
        self.pushButton_summary_process.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_processButton.addWidget(self.pushButton_summary_process)


        self.verticalLayout_summary.addLayout(self.horizontalLayout_processButton)


        self.horizontalLayout_tab_summary.addLayout(self.verticalLayout_summary)

        self.horizontalSpacer_3 = QSpacerItem(50, 5, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_tab_summary.addItem(self.horizontalSpacer_3)

        self.verticalLayout_videoPreview = QVBoxLayout()
        self.verticalLayout_videoPreview.setObjectName(u"verticalLayout_videoPreview")
        self.label_videoPreview_description = QLabel(self.tab_summary)
        self.label_videoPreview_description.setObjectName(u"label_videoPreview_description")
        sizePolicy4.setHeightForWidth(self.label_videoPreview_description.sizePolicy().hasHeightForWidth())
        self.label_videoPreview_description.setSizePolicy(sizePolicy4)
        self.label_videoPreview_description.setFont(font)

        self.verticalLayout_videoPreview.addWidget(self.label_videoPreview_description)

        self.label_videoPreview_image = QLabel(self.tab_summary)
        self.label_videoPreview_image.setObjectName(u"label_videoPreview_image")
        sizePolicy3.setHeightForWidth(self.label_videoPreview_image.sizePolicy().hasHeightForWidth())
        self.label_videoPreview_image.setSizePolicy(sizePolicy3)
        self.label_videoPreview_image.setMinimumSize(QSize(640, 360))
        self.label_videoPreview_image.setMaximumSize(QSize(16777215, 16777215))
        self.label_videoPreview_image.setFrameShape(QFrame.Box)
        self.label_videoPreview_image.setFrameShadow(QFrame.Plain)
        self.label_videoPreview_image.setLineWidth(1)
        self.label_videoPreview_image.setScaledContents(True)
        self.label_videoPreview_image.setAlignment(Qt.AlignCenter)

        self.verticalLayout_videoPreview.addWidget(self.label_videoPreview_image)

        self.horizontalLayout_videoPreview_control = QHBoxLayout()
        self.horizontalLayout_videoPreview_control.setObjectName(u"horizontalLayout_videoPreview_control")
        self.pushButton_videoPreview_prev = QPushButton(self.tab_summary)
        self.pushButton_videoPreview_prev.setObjectName(u"pushButton_videoPreview_prev")
        self.pushButton_videoPreview_prev.setEnabled(False)

        self.horizontalLayout_videoPreview_control.addWidget(self.pushButton_videoPreview_prev)

        self.pushButton_videoPreview_next = QPushButton(self.tab_summary)
        self.pushButton_videoPreview_next.setObjectName(u"pushButton_videoPreview_next")
        self.pushButton_videoPreview_next.setEnabled(False)

        self.horizontalLayout_videoPreview_control.addWidget(self.pushButton_videoPreview_next)


        self.verticalLayout_videoPreview.addLayout(self.horizontalLayout_videoPreview_control)


        self.horizontalLayout_tab_summary.addLayout(self.verticalLayout_videoPreview)


        self.gridLayout.addLayout(self.horizontalLayout_tab_summary, 0, 0, 1, 1)

        self.tabWidget_content.addTab(self.tab_summary, "")
        self.tab_details = QWidget()
        self.tab_details.setObjectName(u"tab_details")
        self.gridLayout_2 = QGridLayout(self.tab_details)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_detailsTab = QHBoxLayout()
        self.horizontalLayout_detailsTab.setObjectName(u"horizontalLayout_detailsTab")
        self.verticalLayout_indexedList = QVBoxLayout()
        self.verticalLayout_indexedList.setObjectName(u"verticalLayout_indexedList")
        self.label_indexedPeople_description = QLabel(self.tab_details)
        self.label_indexedPeople_description.setObjectName(u"label_indexedPeople_description")
        sizePolicy2.setHeightForWidth(self.label_indexedPeople_description.sizePolicy().hasHeightForWidth())
        self.label_indexedPeople_description.setSizePolicy(sizePolicy2)
        self.label_indexedPeople_description.setFont(font)

        self.verticalLayout_indexedList.addWidget(self.label_indexedPeople_description)

        self.listView_indexedPeople = QListView(self.tab_details)
        self.listView_indexedPeople.setObjectName(u"listView_indexedPeople")
        self.listView_indexedPeople.setFrameShape(QFrame.Box)
        #self.listView_indexedPeople.setViewMode()

        self.verticalLayout_indexedList.addWidget(self.listView_indexedPeople)

        self.horizontalLayout_detailsTab.addLayout(self.verticalLayout_indexedList)

        self.horizontalSpacer_4 = QSpacerItem(15, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_detailsTab.addItem(self.horizontalSpacer_4)

        self.verticalLayout_framePreview = QVBoxLayout()
        self.verticalLayout_framePreview.setObjectName(u"verticalLayout_framePreview")
        self.label_framePreview_description = QLabel(self.tab_details)
        self.label_framePreview_description.setObjectName(u"label_framePreview_description")
        sizePolicy3.setHeightForWidth(self.label_framePreview_description.sizePolicy().hasHeightForWidth())
        self.label_framePreview_description.setSizePolicy(sizePolicy3)
        self.label_framePreview_description.setFont(font)

        self.verticalLayout_framePreview.addWidget(self.label_framePreview_description)

        self.label_framePreview_image = QLabel(self.tab_details)
        self.label_framePreview_image.setObjectName(u"label_framePreview_image")
        sizePolicy3.setHeightForWidth(self.label_framePreview_image.sizePolicy().hasHeightForWidth())
        self.label_framePreview_image.setSizePolicy(sizePolicy3)
        self.label_framePreview_image.setMinimumSize(QSize(320, 180))
        self.label_framePreview_image.setMaximumSize(QSize(16777215, 16777215))
        self.label_framePreview_image.setFrameShape(QFrame.Box)
        self.label_framePreview_image.setFrameShadow(QFrame.Plain)
        self.label_framePreview_image.setLineWidth(1)
        self.label_framePreview_image.setScaledContents(True)
        self.label_framePreview_image.setAlignment(Qt.AlignCenter)

        self.verticalLayout_framePreview.addWidget(self.label_framePreview_image)

        self.groupBox_montagePanel = QGroupBox(self.tab_details)
        self.groupBox_montagePanel.setObjectName(u"groupBox_montagePanel")
        self.groupBox_montagePanel.setFont(font1)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_montagePanel)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_controlPanel = QVBoxLayout()
        self.verticalLayout_controlPanel.setObjectName(u"verticalLayout_controlPanel")
        self.verticalLayout_radioSelection = QVBoxLayout()
        self.verticalLayout_radioSelection.setObjectName(u"verticalLayout_radioSelection")
        self.radioButton_montagePanel_all = QRadioButton(self.groupBox_montagePanel)
        self.radioButton_montagePanel_all.setObjectName(u"radioButton_montagePanel_all")

        self.verticalLayout_radioSelection.addWidget(self.radioButton_montagePanel_all)

        self.radioButton_montagePanel_selected = QRadioButton(self.groupBox_montagePanel)
        self.radioButton_montagePanel_selected.setObjectName(u"radioButton_montagePanel_selected")

        self.verticalLayout_radioSelection.addWidget(self.radioButton_montagePanel_selected)

        self.verticalSpacer_7 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_radioSelection.addItem(self.verticalSpacer_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_montagePanel_create = QPushButton(self.groupBox_montagePanel)
        self.pushButton_montagePanel_create.setObjectName(u"pushButton_montagePanel_create")
        sizePolicy3.setHeightForWidth(self.pushButton_montagePanel_create.sizePolicy().hasHeightForWidth())
        self.pushButton_montagePanel_create.setSizePolicy(sizePolicy3)
        self.pushButton_montagePanel_create.setMinimumSize(QSize(120, 0))

        self.horizontalLayout.addWidget(self.pushButton_montagePanel_create)


        self.verticalLayout_radioSelection.addLayout(self.horizontalLayout)


        self.verticalLayout_controlPanel.addLayout(self.verticalLayout_radioSelection)


        self.verticalLayout_3.addLayout(self.verticalLayout_controlPanel)

        self.groupBox_montagePanel_controlPanel = QGroupBox(self.groupBox_montagePanel)
        self.groupBox_montagePanel_controlPanel.setObjectName(u"groupBox_montagePanel_controlPanel")
        self.horizontalLayout_9 = QHBoxLayout(self.groupBox_montagePanel_controlPanel)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton_controlPanel_playVideo = QPushButton(self.groupBox_montagePanel_controlPanel)
        self.pushButton_controlPanel_playVideo.setObjectName(u"pushButton_controlPanel_playVideo")

        self.horizontalLayout_9.addWidget(self.pushButton_controlPanel_playVideo)

        self.pushButton_controlPanel_openVideoFolder = QPushButton(self.groupBox_montagePanel_controlPanel)
        self.pushButton_controlPanel_openVideoFolder.setObjectName(u"pushButton_controlPanel_openVideoFolder")

        self.horizontalLayout_9.addWidget(self.pushButton_controlPanel_openVideoFolder)


        self.verticalLayout_3.addWidget(self.groupBox_montagePanel_controlPanel)


        self.verticalLayout_framePreview.addWidget(self.groupBox_montagePanel)


        self.horizontalLayout_detailsTab.addLayout(self.verticalLayout_framePreview)

        self.horizontalSpacer_5 = QSpacerItem(15, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_detailsTab.addItem(self.horizontalSpacer_5)

        self.verticalLayout_personCropPreview = QVBoxLayout()
        self.verticalLayout_personCropPreview.setObjectName(u"verticalLayout_personCropPreview")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, -1, -1, -1)
        self.label_personCropPreviewDescription = QLabel(self.tab_details)
        self.label_personCropPreviewDescription.setObjectName(u"label_personCropPreviewDescription")
        sizePolicy3.setHeightForWidth(self.label_personCropPreviewDescription.sizePolicy().hasHeightForWidth())
        self.label_personCropPreviewDescription.setSizePolicy(sizePolicy3)
        self.label_personCropPreviewDescription.setFont(font)

        self.horizontalLayout_11.addWidget(self.label_personCropPreviewDescription)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_6)


        self.verticalLayout_personCropPreview.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_personCropPreviewImage = QLabel(self.tab_details)
        self.label_personCropPreviewImage.setObjectName(u"label_personCropPreviewImage")
        sizePolicy3.setHeightForWidth(self.label_personCropPreviewImage.sizePolicy().hasHeightForWidth())
        self.label_personCropPreviewImage.setSizePolicy(sizePolicy3)
        self.label_personCropPreviewImage.setMinimumSize(QSize(180, 320))
        self.label_personCropPreviewImage.setMaximumSize(QSize(16777215, 16777215))
        self.label_personCropPreviewImage.setFrameShape(QFrame.Box)
        self.label_personCropPreviewImage.setFrameShadow(QFrame.Plain)
        self.label_personCropPreviewImage.setLineWidth(1)
        self.label_personCropPreviewImage.setScaledContents(True)
        self.label_personCropPreviewImage.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.label_personCropPreviewImage)


        self.verticalLayout_personCropPreview.addLayout(self.horizontalLayout_8)

        self.label_cropCounter = QLabel(self.tab_details)
        self.label_cropCounter.setObjectName(u"label_cropCounter")
        self.label_cropCounter.setAlignment(Qt.AlignCenter)

        self.verticalLayout_personCropPreview.addWidget(self.label_cropCounter)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_personCropPreview_auto = QPushButton(self.tab_details)
        self.pushButton_personCropPreview_auto.setObjectName(u"pushButton_personCropPreview_auto")

        self.horizontalLayout_7.addWidget(self.pushButton_personCropPreview_auto)

        self.pushButton_personCropPreview_prev = QPushButton(self.tab_details)
        self.pushButton_personCropPreview_prev.setObjectName(u"pushButton_personCropPreview_prev")

        self.horizontalLayout_7.addWidget(self.pushButton_personCropPreview_prev)

        self.pushButton_personCropPreview_next = QPushButton(self.tab_details)
        self.pushButton_personCropPreview_next.setObjectName(u"pushButton_personCropPreview_next")

        self.horizontalLayout_7.addWidget(self.pushButton_personCropPreview_next)


        self.verticalLayout_personCropPreview.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_personCropPreview.addItem(self.verticalSpacer_8)


        self.horizontalLayout_detailsTab.addLayout(self.verticalLayout_personCropPreview)


        self.gridLayout_2.addLayout(self.horizontalLayout_detailsTab, 0, 0, 1, 1)

        self.tabWidget_content.addTab(self.tab_details, "")

        self.verticalLayout.addWidget(self.tabWidget_content)

        self.verticalLayout_statusBar = QVBoxLayout()
        self.verticalLayout_statusBar.setSpacing(0)
        self.verticalLayout_statusBar.setObjectName(u"verticalLayout_statusBar")
        self.label_status = QLabel(self.centralwidget)
        self.label_status.setObjectName(u"label_status")
        sizePolicy2.setHeightForWidth(self.label_status.sizePolicy().hasHeightForWidth())
        self.label_status.setSizePolicy(sizePolicy2)
        self.label_status.setFixedSize(QSize(90, 25))
        #self.label_status.setMinimumSize(QSize(90, 25))
        #self.label_status.setMaximumSize(QSize(90, 25))
        self.label_status.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_status.hide()

        self.verticalLayout_statusBar.addWidget(self.label_status)

        #progressbar
        self.progressBar_status = QProgressBar(self.centralwidget)
        self.progressBar_status.setObjectName(u"progressBar_status")
        sizePolicy6 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.progressBar_status.sizePolicy().hasHeightForWidth())
        self.progressBar_status.setSizePolicy(sizePolicy6)
        self.progressBar_status.setMinimumSize(QSize(0, 20))
        self.progressBar_status.setMaximumSize(QSize(16777215, 25))
        self.progressBar_status.setValue(0)
        self.progressBar_status.setTextVisible(True)
        self.progressBar_status.setInvertedAppearance(False)
        self.progressBar_status.hide()

        self.verticalLayout_statusBar.addWidget(self.progressBar_status)


        self.verticalLayout.addLayout(self.verticalLayout_statusBar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 25))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)

        self.tabWidget_content.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_videoSelection_description.setText(QCoreApplication.translate("MainWindow", u"Title:", None))
        self.pushButton_videoSelection_add.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButton_videoSelection_openFolder.setText(QCoreApplication.translate("MainWindow", u"Open Input Folder", None))
        self.label_presetSelection_description.setText(QCoreApplication.translate("MainWindow", u"Preset:", None))
        self.label_summary_format_description.setText(QCoreApplication.translate("MainWindow", u"Format:", None))
        self.label_summary_format_content.setText(QCoreApplication.translate("MainWindow", u"(video file type)", None))
        self.label_summary_resolution_description.setText(QCoreApplication.translate("MainWindow", u"Resolution:", None))
        self.label_summary_resolution_content.setText(QCoreApplication.translate("MainWindow", u"(resolution size)", None))
        self.label_summary_duration_description.setText(QCoreApplication.translate("MainWindow", u"Duration:", None))
        self.label_summary_duration_content.setText(QCoreApplication.translate("MainWindow", u"(00:00:00)", None))
        self.label_summary_framerate_description.setText(QCoreApplication.translate("MainWindow", u"Framerate:", None))
        self.label_summary_framerate_content.setText(QCoreApplication.translate("MainWindow", u"(frame rate)", None))
        self.label_summary_frames_description.setText(QCoreApplication.translate("MainWindow", u"Frames:", None))
        self.label_summary_frames_content.setText(QCoreApplication.translate("MainWindow", u"(frames)", None))
        self.label_summary_processed_Description.setText(QCoreApplication.translate("MainWindow", u"Already Processed:", None))
        self.label_summary_processed_content.setText(QCoreApplication.translate("MainWindow", u"(Yes/No)", None))
        self.pushButton_summary_process.setText(QCoreApplication.translate("MainWindow", u"Process", None))
        self.label_videoPreview_description.setText(QCoreApplication.translate("MainWindow", u"Video Preview:", None))
        self.label_videoPreview_image.setText(QCoreApplication.translate("MainWindow", u"Preview", None))
        self.pushButton_videoPreview_prev.setText(QCoreApplication.translate("MainWindow", u"Prev", None))
        self.pushButton_videoPreview_next.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.tabWidget_content.setTabText(self.tabWidget_content.indexOf(self.tab_summary), QCoreApplication.translate("MainWindow", u"Summary", None))
        self.label_indexedPeople_description.setText(QCoreApplication.translate("MainWindow", u"List of Detected People:", None))
        self.label_framePreview_description.setText(QCoreApplication.translate("MainWindow", u"Frame Preview:", None))
        self.label_framePreview_image.setText(QCoreApplication.translate("MainWindow", u"Preview", None))
        self.groupBox_montagePanel.setTitle(QCoreApplication.translate("MainWindow", u"Montage Panel", None))
        self.radioButton_montagePanel_all.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.radioButton_montagePanel_selected.setText(QCoreApplication.translate("MainWindow", u"Selected", None))
        self.pushButton_montagePanel_create.setText(QCoreApplication.translate("MainWindow", u"Create Montage", None))
        self.groupBox_montagePanel_controlPanel.setTitle(QCoreApplication.translate("MainWindow", u"Control Panel", None))
        self.pushButton_controlPanel_playVideo.setText(QCoreApplication.translate("MainWindow", u"Play Video", None))
        self.pushButton_controlPanel_openVideoFolder.setText(QCoreApplication.translate("MainWindow", u"Open Video Folder", None))
        self.label_personCropPreviewDescription.setText(QCoreApplication.translate("MainWindow", u"Person Crop Preview:", None))
        self.label_personCropPreviewImage.setText(QCoreApplication.translate("MainWindow", u"Preview", None))
        self.label_cropCounter.setText(QCoreApplication.translate("MainWindow", u"(0/0)", None))
        self.pushButton_personCropPreview_auto.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.pushButton_personCropPreview_prev.setText(QCoreApplication.translate("MainWindow", u"Prev", None))
        self.pushButton_personCropPreview_next.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.tabWidget_content.setTabText(self.tabWidget_content.indexOf(self.tab_details), QCoreApplication.translate("MainWindow", u"Details", None))
        self.label_status.setText(QCoreApplication.translate("MainWindow", u"Processing....", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi
