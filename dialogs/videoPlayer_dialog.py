from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QSlider, QHBoxLayout
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

# Dialog para mostrar el video de InfoView
class VideoPlayerDialog(QDialog):
    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle("Video Explicativo")
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color: #2E2E2E; border-radius: 15px;")

        # Centrar ventana en pantalla
        self.move(
            (self.screen().availableGeometry().width() - self.width()) // 2,
            (self.screen().availableGeometry().height() - self.height()) // 2
        )

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Reproductor de video
        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("border: 4px solid #FF8C00; border-radius: 8px;")
        layout.addWidget(self.video_widget)

        # Controlador del video
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.media_player.setVideoOutput(self.video_widget)

        # Barra de progreso del video
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setStyleSheet("QSlider::groove:horizontal { background: #FF8C00; height: 6px; border-radius: 3px; }"
                                 "QSlider::handle:horizontal { background: #FFFFFF; width: 14px; margin: -4px 0; border-radius: 7px; }")
        self.slider.sliderMoved.connect(self.set_position)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        layout.addWidget(self.slider)

        # Controles de reproducción con botones redondeados y naranja
        controls_layout = QHBoxLayout()

        btn_play = QPushButton(QIcon("images/playVideo.png"), "")
        btn_play.setToolTip("Reproducir")
        btn_play.setStyleSheet("background-color: #FF8C00; border-radius: 15px; padding: 8px;")
        btn_play.clicked.connect(self.media_player.play)
        controls_layout.addWidget(btn_play)

        btn_pause = QPushButton(QIcon("images/pauseVideo.png"), "")
        btn_pause.setToolTip("Pausar")
        btn_pause.setStyleSheet("background-color: #FF8C00; border-radius: 15px; padding: 8px;")
        btn_pause.clicked.connect(self.media_player.pause)
        controls_layout.addWidget(btn_pause)

        btn_stop = QPushButton(QIcon("images/stopVideo.png"), "")
        btn_stop.setToolTip("Detener")
        btn_stop.setStyleSheet("background-color: #FF8C00; border-radius: 15px; padding: 8px;")
        btn_stop.clicked.connect(self.media_player.stop)
        controls_layout.addWidget(btn_stop)

        layout.addLayout(controls_layout)

        # Iniciar el video automáticamente
        self.media_player.play()


    # Funciones para pausar, reanudar y empezar el video
    def set_position(self, position):
        self.media_player.setPosition(int(position * self.media_player.duration() / 100))

    def update_position(self, position):
        if self.media_player.duration() > 0:
            self.slider.setValue(int((position / self.media_player.duration()) * 100))

    def update_duration(self, duration):
        self.slider.setRange(0, 100)