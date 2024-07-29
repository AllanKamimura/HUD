from PySide2.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt, QThread, Signal, QByteArray, QDataStream, QBuffer

import numpy as np

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

import sys
# Initialize GStreamer
Gst.init(None)


class VideoThread(QThread):
    frame_data_signal = Signal(bytes)
    width  = 1280
    height = 720

    def __init__(self, parent=None):
        super(VideoThread, self).__init__(parent)
        self.pipeline = None

    def run(self):
        # Set up the GStreamer pipeline
        self.pipeline = Gst.parse_launch(
            f"v4l2src device=/dev/video0 ! videoconvert ! video/x-raw,format=RGB,width={self.width},height={self.height} ! appsink name=sink emit-signals=True"
        )

        appsink = self.pipeline.get_by_name("sink")
        appsink.connect("new-sample", self.on_new_sample, appsink)

        # Start playing
        self.pipeline.set_state(Gst.State.PLAYING)

        # Run the GStreamer main loop
        loop = GObject.MainLoop()
        loop.run()

    def on_new_sample(self, sink, data):
        sample = sink.emit("pull-sample")
        if sample:
            buffer = sample.get_buffer()

            # Map the buffer to a readable format
            success, map_info = buffer.map(Gst.MapFlags.READ)
            if success:
                frame_data = map_info.data
                print(type(frame_data))
                self.frame_data_signal.emit(bytes(frame_data))

                # Unmap the buffer
                buffer.unmap(map_info)

            return Gst.FlowReturn.OK

    def stop_pipeline(self):
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)

class VideoPlayer(QWidget):
    width  = 1280
    height = 720

    def __init__(self):
        super(VideoPlayer, self).__init__()

        self.video_thread = VideoThread(self)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.video_thread.frame_data_signal.connect(self.update_frame)
        self.video_thread.start()

    def update_frame(self, frame_data):
        # Convert frame data to a NumPy array
        # frame_array = np.frombuffer(frame_data.data(), dtype=np.uint8).reshape((self.height, self.width, 3))
        # frame_rgb = (frame_array).copy(order='C')

        qimage = QImage(frame_data, self.width, self.height, QImage.Format_RGB888)

        # Set the image in the QLabel
        pixmap = QPixmap.fromImage(qimage)

        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.video_thread.stop_pipeline()
        self.video_thread.wait()
        event.accept()