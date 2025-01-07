import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsView, QGraphicsScene

from src.visualization.animation import BikeAnimation
from src.visualization.perpetual_animation import PerpetualAnimation
from src.visualization.playstate import PlayState
from src.visualization.renderer import draw_back_view, draw_birds_eye_view
from src.visualization.BikeScenes import BirdEyeBikeScene, RearViewBikeScene


class BikeAnimationWindow(QMainWindow):
    animation: BikeAnimation = None
    play_state: PlayState = None
    animation_timer: QTimer = None
    animation_delay_ms = 33

    bird_eye_scene: BirdEyeBikeScene
    back_view: RearViewBikeScene

    def __init__(self, animation: BikeAnimation):
        super().__init__()

        # init state
        self.play_state = PlayState()
        self.animation = animation

        self.setWindowTitle('Visualization')
        self.setGeometry(100, 100, 800, 600)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layouts
        main_layout = QVBoxLayout()
        canvas_layout = QHBoxLayout()
        control_layout = QHBoxLayout()

        # Scenes
        self.bird_eye_scene = BirdEyeBikeScene()
        self.back_view = RearViewBikeScene()

        # Canvases
        self.canvas1 = QGraphicsView()
        self.canvas1.setScene(self.bird_eye_scene)
        self.canvas1.setFrameShape(QGraphicsView.NoFrame)
        self.canvas1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.canvas1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.canvas1.setRenderHint(QPainter.Antialiasing)
        self.canvas1.setMinimumSize(400, 400)

        self.canvas2 = QGraphicsView()
        self.canvas2.setScene(self.back_view)
        self.canvas2.setFrameShape(QGraphicsView.NoFrame)
        self.canvas2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.canvas2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.canvas2.setRenderHint(QPainter.Antialiasing)
        self.canvas2.setMinimumSize(400, 400)

        canvas_layout.addWidget(self.canvas1)
        canvas_layout.addWidget(self.canvas2)

        # Control buttons
        self.step_back_button = QPushButton('Step Back')
        self.play_pause_button = QPushButton('Play')
        self.step_forward_button = QPushButton('Step Forward')

        control_layout.addWidget(self.step_back_button)
        control_layout.addWidget(self.play_pause_button)
        control_layout.addWidget(self.step_forward_button)

        # Connect buttons to dummy listeners
        self.step_back_button.clicked.connect(self.step_back)
        self.play_pause_button.clicked.connect(self.play_pause)
        self.step_forward_button.clicked.connect(self.step_forward)

        # Add layouts to main layout
        main_layout.addLayout(canvas_layout)
        main_layout.addLayout(control_layout)

        main_widget.setLayout(main_layout)

        # Timer for animation
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.step_forward)

    def update_canvas(self):
        animation_state = self.animation.get_state_at_frame(self.play_state.frame)
        self.bird_eye_scene.update_bike(animation_state)
        self.back_view.update_bike(animation_state)

    def play_pause(self):
        if self.play_state.playing:
            self.play_state.playing = False
            self.play_pause_button.setText('Play')
            self.animation_timer.stop()
        else:
            self.play_state.playing = True
            self.play_pause_button.setText('Pause')
            self.animation_timer.start(self.animation_delay_ms)

    def step_forward(self):
        self.play_state.step_forward()
        self.update_canvas()

    def step_back(self):
        self.play_state.step_back()
        self.update_canvas()

    def get_play_state(self):
        return self.play_state

# Main function
def main():
    app = QApplication(sys.argv)
    window = BikeAnimationWindow(PerpetualAnimation())
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()