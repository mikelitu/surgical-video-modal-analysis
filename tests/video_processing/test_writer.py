import unittest
from pymodal_surgical.video_processing.writer import VideoWriter
import numpy as np
from pymodal_surgical.video_processing.reader import VideoReader, RetType
from pathlib import Path
import shutil

script_dir = Path(__file__).resolve().parent


class TestVideoWriter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.save_path = script_dir/"video_test"
        cls.save_path.mkdir(exist_ok=True, parents=True)
        video_config_dic = {
            "output_mono": {
                "video_path": cls.save_path/"output_mono.mp4",
                "fps": 30,
                "video_type": "mono"
            },
            "output_stereo": {
                "video_path": cls.save_path/"output_stereo.mp4",
                "fps": 30,
                "video_type": "stereo"
            }
        }
        cls.reader_video_config = video_config_dic

    def test_write_mono(self):
        # Create a VideoWriter instance
        video_path = self.save_path/"output_mono.mp4"
        video_config = {"video_path": video_path, "fps": 30, "video_type": "mono"}
        writer = VideoWriter(video_config)

        # Generate some dummy frames
        frames = np.random.randint(0, 255, size=(10, 480, 640, 3), dtype=np.uint8)

        # Call the __call__ method to write the frames
        writer(frames)

        # Add assertion to verify that the file exists
        self.assertTrue(video_path.exists())
        self.assertTrue(video_path.is_file())
        self.assertTrue(video_path.stat().st_size > 0)
        self.assertTrue(video_path.suffix == ".mp4")

        # Open the video and verify the number of frames
        reader = VideoReader(self.reader_video_config["output_mono"], return_type=RetType.NUMPY)
        self.assertEqual(len(reader), 10)
        self.assertEqual(reader.video_type, "mono")
        self.assertEqual(reader.fps, 30)
        reader._close()


    def test_write_stereo(self):
        # Create a VideoWriter instance
        video_path = self.save_path/"output_stereo.mp4"
        video_config = {"video_path": video_path, "fps": 30, "video_type": "stereo"}
        writer = VideoWriter(video_config)

        # Generate some dummy frames
        frames_left = np.random.randint(0, 255, size=(10, 480, 640, 3), dtype=np.uint8)
        frames_right = np.random.randint(0, 255, size=(10, 480, 640, 3), dtype=np.uint8)
        frames = (frames_left, frames_right)

        # Call the __call__ method to write the frames
        writer(frames)

        # TODO: Add assertions to verify the output file
        # Add assertion to verify that the file exists
        self.assertTrue(video_path.exists())
        self.assertTrue(video_path.is_file())
        self.assertTrue(video_path.stat().st_size > 0)
        self.assertTrue(video_path.suffix == ".mp4")

        # Open the video and verify the number of frames
        reader = VideoReader(self.reader_video_config["output_stereo"], return_type=RetType.NUMPY)
        self.assertEqual(len(reader), 10)
        self.assertEqual(reader.video_type, "stereo")
        self.assertEqual(reader.fps, 30)
        reader._close()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.save_path)

if __name__ == "__main__":
    unittest.main()