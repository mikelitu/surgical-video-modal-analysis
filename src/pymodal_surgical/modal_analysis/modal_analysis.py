import torch


def mode_shapes_from_optical_flow(
    flow_field: torch.Tensor, 
    K: int,
    timestep: int
) -> torch.Tensor:
    
    if len(flow_field.shape) == 4:
        flow_field = flow_field.view(-1, timestep, flow_field.shape[1], flow_field.shape[2], flow_field.shape[3])

    batch_size, _, dim, height, width = flow_field.shape
    if dim not in [2, 3]:
        raise ValueError("The dimension of the flow field must be 2 for 2D tensors or 3 for 3D tensors.")
    
    motion_texture = torch.zeros((batch_size, K, 4 if dim==2 else 6, height, width)).to(flow_field.device)
    for i in range(height):
        for j in range(width):
            x_t = flow_field[:, :, 0, i, j]
            y_t = flow_field[:, :, 1, i, j]
            Y_f = torch.fft.rfft(x_t, timestep, dim=-1)
            X_f = torch.fft.rfft(y_t, timestep, dim=-1)
            motion_texture[:, :, 0, i, j] = (1.0 / K) * X_f[:, 1:K+1].real
            motion_texture[:, :, 1, i, j] = (1.0 / K) * X_f[:, 1:K+1].imag
            motion_texture[:, :, 2, i, j] = (1.0 / K) * Y_f[:, 1:K+1].real
            motion_texture[:, :, 3, i, j] = (1.0 / K) * Y_f[:, 1:K+1].imag
            if dim == 3:
                z_t = flow_field[:, :, 2, i, j]
                Z_f = torch.fft.rfft(z_t, timestep, dim=-1)
                motion_texture[:, :, 4, i, j] = (1.0 / K) * Z_f[:, 1:K+1].real
                motion_texture[:, :, 5, i, j] = (1.0 / K) * Z_f[:, 1:K+1].imag

    return motion_texture


def get_motion_frequencies(
    timesteps: int,
    K: int,
    sampling_period: float
) -> torch.Tensor:
    """
    Compute the motion frequencies.

    Args:
        timesteps (int): Number of timesteps.
        K (int): Number of frequencies.
        sample_rate (float): The sample rate.

    Returns:
        frequencies (torch.Tensor): Tensor of shape (K,) and dtype torch.float.
    """

    frequency_spacing = 1.0 / (timesteps * sampling_period)
    frequencies = torch.fft.fftfreq(timesteps, d=sampling_period)[1:K+1]
    return 2 * torch.pi * (frequencies * frequency_spacing)


def calculate_modal_magnitude(
    mode_shape: torch.Tensor, 
    displacement: torch.Tensor,
    pixel: tuple[int, int],
    alpha: float = 1.0
) -> torch.Tensor:
    """
    Calculate the modal coordinate magnitude from the mode shape and displacement.
    """

    # Calculate the modal coordinate
    displacement = displacement.unsqueeze(1).T
    displacement = displacement.repeat(mode_shape.shape[0], 1)
    mode_pixel = mode_shape[:, :, *pixel]
    batch_mm = (displacement * mode_pixel).abs()
    return batch_mm * alpha


def calculate_modal_phase(
    mode_shape: torch.Tensor, 
    displacement: torch.Tensor,
    pixel: tuple[int, int],
    maximize: str = "disp"
) -> torch.Tensor:
    """
    Calculate the modal coordinate from the mode shape and displacement.
    """
    if maximize not in ["disp", "velocity"]:
        raise ValueError("maximize must be 'disp' or 'velocity'")
    # Get the displacement at the correct shape
    displacement = displacement.unsqueeze(1).T
    displacement = displacement.repeat(mode_shape.shape[0], 1)
    # Get the mode shape at the correct pixel
    mode_pixel = mode_shape[:, :, *pixel]
    # Get the phase of the dot product
    angles = torch.angle(displacement * mode_pixel)
    if maximize == "disp":
        return -angles
    else:
        return -angles + torch.pi/2