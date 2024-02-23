import cv2
import numpy as np
from pathlib import Path, PosixPath
from enum import Enum
import torch

class VideoType(str, Enum):
    STEREO = "stereo"
    MONO = "mono"

class RetType(str, Enum):
    NUMPY = "numpy"
    TENSOR = "tensor"
    LIST = "list"


class VideoReader(object):

    def __init__(
        self,
        video_path: str | PosixPath,
        video_config: dict[str, VideoType | str | PosixPath],
        return_type: RetType | str = RetType.NUMPY,
    ) -> None:
        
        if not isinstance(video_path, PosixPath):
            video_path = Path(video_path)

        self.cap = self._open_video(video_path)
        self.video_path = video_path
        self.video_config = video_config
        self.video_length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_type = video_config[video_path.stem]["video_type"]
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._reading_method = self._read_mono if self.video_type == VideoType.MONO else self._read_stereo
        self._frame_reading_method = self._read_mono_frame if self.video_type == VideoType.MONO else self._read_stereo_frame
        self._return_func = {RetType.NUMPY: self._return_numpy, RetType.TENSOR: self._return_tensor, RetType.LIST: self._return_list}[return_type]
    
    def _read_mono(self, start: int = 0, end: int = 0) -> list[np.ndarray]:
        if end == 0:
            end = self.video_length
        elif end > self.video_length:
            raise ValueError(f"End frame number out of range, for video of length {self.video_length}")
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        frames = []
        for _ in range(start, end):
            ret, frame = self.cap.read()
            if ret:
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                break
        return frames
    
    def _read_stereo(self, start: int = 0, end: int = 0) -> tuple[list[np.ndarray], list[np.ndarray]]:
        if end == 0:
            end = self.video_length
        elif end > self.video_length:
            raise ValueError(f"End frame number out of range, for video of length {self.video_length}")
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        left_frames, right_frames = [], []
        for _ in range(start, end):
            ret, frame = self.cap.read()
            if ret:
                half_width = self.width // 2
                left_frame = frame[:, :half_width, :]
                right_frame = frame[:, half_width:, :]
                left_frames.append(cv2.cvtColor(left_frame, cv2.COLOR_BGR2RGB))
                right_frames.append(cv2.cvtColor(right_frame, cv2.COLOR_BGR2RGB))
            else:
                break
        return left_frames, right_frames

    def read(self, start: int = 0, end: int = 0) -> list[np.ndarray] | tuple[list[np.ndarray], list[np.ndarray]]:
        return self._return_func(self._reading_method(start, end))
    
    def read_frame(self, frame_number: int) -> np.ndarray | tuple[np.ndarray, np.ndarray]:
        return self._return_func(self._frame_reading_method(frame_number))
    
    def _read_mono_frame(self, frame_number: int) -> np.ndarray:
        if frame_number > self.video_length:
            raise ValueError(f"Frame number out of range, for video of length {self.video_length}")
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            raise ValueError(f"Frame number out of range, for video of length {self.video_length}")
    
    def _read_stereo_frame(self, frame_number: int) -> tuple[np.ndarray, np.ndarray]:
        if frame_number > self.video_length:
            raise ValueError(f"End frame number out of range, for video of length {self.video_length}")
    
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        if ret:
            half_width = self.width // 2
            left_frame = frame[:, :half_width, :]
            right_frame = frame[:, half_width:, :]
            return cv2.cvtColor(left_frame, cv2.COLOR_BGR2RGB), cv2.cvtColor(right_frame, cv2.COLOR_BGR2RGB)
        else:
            raise ValueError(f"Frame number out of range, for video of length {self.video_length}")
    
    def _return_numpy(
        self, 
        frames: list[np.ndarray] | tuple[list[np.ndarray], list[np.ndarray]]
    ) -> np.ndarray | tuple[np.ndarray, np.ndarray]:
        
        if isinstance(frames, tuple):
            return np.stack(frames[0]), np.stack(frames[1])
        else:
            return np.stack(frames)
        
    def _return_tensor(
        self, 
        frames: list[np.ndarray] | tuple[list[np.ndarray], list[np.ndarray]]
    ) -> torch.Tensor | tuple[torch.Tensor, torch.Tensor]:
        
        if isinstance(frames, tuple):
            left_frames = [torch.tensor(frame).permute(2, 0, 1) for frame in frames[0]]
            right_frames = [torch.tensor(frame).permute(2, 0, 1) for frame in frames[1]]
            return torch.stack(left_frames), torch.stack(right_frames)
        else:
            frames = [torch.tensor(frame).permute(2, 0, 1) for frame in frames]
            return torch.stack(frames)
        
    def _return_list(
        self, 
        frames: list[np.ndarray] | tuple[list[np.ndarray], list[np.ndarray]]
    ) -> list[np.ndarray] | tuple[list[np.ndarray], list[np.ndarray]]:
        return frames
    
    def _close(self) -> None:
        self.cap.release()
    
    def _open_video(self, video_path: PosixPath | str) -> cv2.VideoCapture:
        return cv2.VideoCapture(str(video_path))
    
    def __len__(self) -> int:
        return self.video_length
    