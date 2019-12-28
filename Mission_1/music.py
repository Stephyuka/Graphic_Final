from PyQt5 import QtGui
from PyQt5.QtWidgets import QOpenGLWidget,QApplication, QWidget, QHBoxLayout
from PyQt5.QtCore import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtOpenGL import QGLWidget

import sys
import os
import numpy as np
import librosa
import librosa.display

class main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.init_window()

    def init_window(self):
        self.window = gl_window()
        layout = QHBoxLayout()
        layout.addWidget(self.window)
        self.setLayout(layout)
        self.setWindowTitle('Music')
        self.window.end_signal.connect(self.close_down)
        # pygame.mixer.init()
        # pygame.mixer.music.load(sys.argv[1])
        # pygame.mixer.music.play()
        self.show()

    def close_down(self):
        self.close()


class gl_window(QGLWidget):
    end_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_window()

    def resizeGL(self, w, h):
        print('resize')
        glViewport(0, 0, w, h)


    def init_window(self):
        self.setMinimumSize(800,800)
        nargin = len(sys.argv)
        if nargin < 2:
            print('Please set your input music')
            self.end_signal.emit()
            mf.load("/Users/tr/Desktop/music/Coka.mp3")
            mf.get_cqt()
            self.method = 1
        elif nargin == 2:
            path = sys.argv[1]
            if not os.path.isfile(path):
                raise ImportError("The filepath is invalid")
            try:
                mf.load(path)
            except AttributeError:
                raise ImportError("The audio file is invalid")
            mf.get_log_Mel()
            self.method = 1
        elif nargin == 3:
            path = sys.argv[1]
            if not os.path.isfile(path):
                raise ImportError("The filepath is invalid")
            try:
                mf.load(path)
            except AttributeError:
                raise ImportError("The audio file is invalid")
            if sys.argv[2] == '-pitch1':
                mf.get_cqt()
                self.method = 1
            elif sys.argv[2] == '-pitch2':
                mf.get_log_Mel()
                self.method = 1
            elif sys.argv[2] == '-tempo':
                mf.get_tempo()
                self.method = 1
            else:
                if sys.argv[2] == '-l':
                    self.method = 0
                    mf.get_log_Mel()
                elif sys.argv[2] == '-p':
                    self.method = 1
                    mf.get_log_Mel()
                else:
                    raise Exception('The function doesn\'t exist')
        elif nargin == 4:
            path = sys.argv[1]
            if not os.path.isfile(path):
                raise ImportError("The filepath is invalid")
            try:
                mf.load(path)
            except AttributeError:
                raise ImportError("The audio file is invalid")
            if sys.argv[2] == '-pitch1':
                mf.get_cqt()
            elif sys.argv[2] == '-pitch2':
                mf.get_log_Mel()
            elif sys.argv[2] == '-tempo':
                mf.get_tempo()
            else:
                raise Exception('The Method doesn\'t exist')
            if sys.argv[3] == '-p':
                self.method = 1
            elif sys.argv[3] == '-l':
                self.method = 0
        self.start = 0
        # self.file_path = sys.argv[1]


    def paintGL(self):
        pt.refresh(mf.box, mf.n_mels, self.start)
        if self.method:
            pt.act_point()
        else:
            pt.act()

    def updateGL(self):
        self.start += 1
        if self.start == mf.length:
            self.end_signal.emit()
        else:
            self.glDraw()


class music_proc:
    def __init__(self):
        self.n_fft = 4096
        self.hop_length = 512
        self.n_mels = 128

    def load(self, file):
        self.music, self.sr = librosa.load(path=file, sr=44100)

    def get_tempo(self):
        self.tempo = librosa.feature.fourier_tempogram(self.music, self.sr, win_length=self.n_mels * 2)
        self.box = librosa.power_to_db(self.tempo) * 5
        print(self.box)
        self.length = self.box.shape[1]

    def get_cqt(self):
        self.cqt = librosa.feature.chroma_cqt(self.music, self.sr,n_chroma = self.n_mels)
        self.box = np.abs(librosa.power_to_db(self.cqt)) * 3.5
        print(self.box)
        self.length = self.box.shape[1]

    def get_log_Mel(self):
        self.melspec = librosa.feature.melspectrogram(self.music, self.sr, n_fft=self.n_fft, n_mels=self.n_mels)
        self.box = librosa.power_to_db(self.melspec)
        self.length = self.box.shape[1]


class particle:
    def __init__(self):
        self.color = np.ndarray([0,0,1],dtype= float)
        self.pos = np.ndarray([0,0,0],dtype= float)
        self.angle = float(0)
        self.accel =  np.ndarray([0,0,0],dtype= float)
        self.v = np.ndarray([0,0,0],dtype= float)


class particle_system:
    def __init__(self, n):
        self.n = n
        self.sphere = gluNewQuadric()
        delta_degree = (float)(360 / (n - 1)) * np.pi / 180
        colors = [[0,0,1,1], [1,0,1,1]]
        self.particles = []
        for i in range(self.n):
            temp = particle()
            temp.angle = i * delta_degree
            temp.pos = [np.cos(temp.angle) / 2, np.sin(temp.angle) / 2, 0]
            temp.color = [(colors[0][0] + (colors[1][0] - colors[0][0]) * np.cos(temp.angle)), (colors[0][1] + (colors[1][1] - colors[0][1]) * np.cos(temp.angle)), (colors[0][2] + (colors[1][2] - colors[0][2]) * np.cos(temp.angle))]
            self.particles.append(temp)


    def refresh(self, spec, n, start):
        smooth = 3
        j = 0
        for i in range(self.n - smooth):
            x = np.fabs(spec[j][start] * np.cos(self.particles[i].angle) / 550 + np.cos(self.particles[i].angle) / 2)
            y = np.fabs(spec[j][start] * np.sin(self.particles[i].angle) / 550 + np.sin(self.particles[i].angle) / 2)
            if np.cos(self.particles[i].angle) < 0:
                x *= -1
            if np.sin(self.particles[i].angle) < 0:
                y *= -1
            self.particles[i].pos = [x, y, 0]
            j += 1


        first = spec[0][start]
        last = spec[self.n - smooth][start]
        for i in range(self.n - smooth, self.n):
            v = last + (first - last)/5.0 * (i - self.n + smooth)
            x = np.fabs( v * np.cos(self.particles[i].angle) / 550 + np.cos(self.particles[i].angle) / 2)
            y = np.fabs( v * np.sin(self.particles[i].angle) / 550 + np.sin(self.particles[i].angle) / 2)
            if np.cos(self.particles[i].angle) < 0:
                x *= -1
            if np.sin(self.particles[i].angle) < 0:
                y *= -1
            self.particles[i].pos = [x, y, 0]


    def render(self):
        for i in range(self.n):
            glColor4f(self.particles[i].color[0], self.particles[i].color[1], self.particles[i].color[2], 1)
            glVertex3f(np.cos(self.particles[i].angle) / 2.5, np.sin(self.particles[i].angle)/ 2.5, 0)
            glVertex3f(self.particles[i].pos[0], self.particles[i].pos[1], self.particles[i].pos[2])

        glEnd()

    def render_point(self):
        for i in range(self.n):
            glColor4f(self.particles[i].color[0], self.particles[i].color[1], self.particles[i].color[2], 1)
            glPushMatrix()
            glTranslatef(self.particles[i].pos[0], self.particles[i].pos[1], self.particles[i].pos[2])
            gluSphere(self.sphere, 0.01, 32, 16)
            glPopMatrix()



    def act(self):
        glClearColor(0.8, 0.8, 0.8, 0.8)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, 0.0)
        glLoadIdentity()
        glDepthMask(GL_FALSE)
        glLineWidth(8)
        glBegin(GL_LINES)
        self.render()
        glDepthMask(GL_TRUE)
        glFlush()

    def act_point(self):
        glClearColor(0.8, 0.8, 0.8, 0.8)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, 0.0)
        glLoadIdentity()
        glDepthMask(GL_FALSE)
        glLineWidth(10)
        glBegin(GL_LINES)
        self.render_point()
        glDepthMask(GL_TRUE)
        glFlush()

def change_size(w, h):
    glViewport(0,0,w,h)


pt = particle_system(100)
mf = music_proc()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = main_window()
    loop = QTimer()
    loop.setInterval((float)(mf.hop_length / mf.sr) * 1000)
    loop.timeout.connect(w.window.updateGL)
    loop.start((float)(mf.hop_length / mf.sr) * 1000)
    sys.exit(app.exec_())