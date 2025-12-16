import numpy as np
import uvicorn
from fastapi import FastAPI
from numba import cuda


# Numba CUDA kernel for gradient computation
@cuda.jit
def compute_gradients_kernel(x, y, w, b, grad_w, grad_b, n):
    idx = cuda.grid(1)
    if idx < n:
        pred = w * x[idx] + b
        err = pred - y[idx]
        cuda.atomic.add(grad_w, 0, err * x[idx])
        cuda.atomic.add(grad_b, 0, err)


# Local training function
def train_local():
    N = 1000
    x = np.random.randn(N).astype(np.float32)
    y = (3.5 * x + 2.0 + np.random.randn(N) * 0.1).astype(np.float32)

    w, b = 0.0, 0.0
    lr = 0.01
    epochs = 100

    d_x = cuda.to_device(x)
    d_y = cuda.to_device(y)

    for _ in range(epochs):
        grad_w = np.zeros(1, dtype=np.float32)
        grad_b = np.zeros(1, dtype=np.float32)
        d_grad_w = cuda.to_device(grad_w)
        d_grad_b = cuda.to_device(grad_b)

        threads_per_block = 256
        blocks_per_grid = (N + threads_per_block - 1) // threads_per_block

        compute_gradients_kernel[blocks_per_grid, threads_per_block](
            d_x, d_y, w, b, d_grad_w, d_grad_b, N
        )

        grad_w_val = d_grad_w.copy_to_host()[0]
        grad_b_val = d_grad_b.copy_to_host()[0]

        w -= lr * (2.0 / N) * grad_w_val
        b -= lr * (2.0 / N) * grad_b_val

    return {"w": float(w), "b": float(b)}


# FastAPI app
app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/train")
def train():
    return train_local()
