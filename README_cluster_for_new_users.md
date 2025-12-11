# Cluster Setup and Usage Guide

This guide explains how to set up the environment and run the breathwork transcription pipeline on the cluster.

## 1. Get the code on the cluster

In a terminal on the cluster:

```bash
cd /gs/home/<your-username>
git clone https://github.com/Namsjain01/breathwork-transcription.git
cd breathwork-transcription
```

*Note: Replace `<your-username>` with your actual cluster username.*

## 2. Create your conda environment (CPU only, safe everywhere)

First make a CPU‑only env (works on login and CPU nodes):

```bash
module load conda
conda create -n breathwork-py310 python=3.10 -y
conda activate breathwork-py310
```

Install the core Python packages:

```bash
pip install -r requirements.txt
```

Install CPU PyTorch (works on any node):

```bash
conda install -y pytorch cpuonly -c pytorch
```

Quick check:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
# Should print a version and False
```

At this point you can already run the pipeline on CPU.

## 3. (Optional but recommended) Add GPU support on the GPU node

When you want to use the GPU (RTX 6000), you should:

Start an interactive GPU shell:

```bash
srun --partition=GPUshortx86 --nodelist=esi-svhpc107 --gpus=1 --pty $SHELL
hostname   # should be: esi-svhpc107
```

Activate the same env and upgrade PyTorch to a CUDA build:

```bash
module load conda
conda activate breathwork-py310

conda install -y pytorch pytorch-cuda=11.8 -c pytorch -c nvidia
```

Verify CUDA is visible:

```bash
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available())"
# Expect: no +cpu in version, CUDA version like 11.8, and True
```

Now the same env works on CPU and GPU nodes; on GPU nodes `torch.cuda.is_available()` becomes `True`.

## 4. Run the pipeline

### 4.1. On GPU (fast runs)

From a login node:

```bash
srun --partition=GPUshortx86 --nodelist=esi-svhpc107 --gpus=1 --pty $SHELL
hostname   # esi-svhpc107
```

Then:

```bash
module load conda
conda activate breathwork-py310

cd /gs/home/<your-username>/breathwork-transcription


python pipeline/run_pipeline.py --input "input_file_path"
```


Your code auto‑selects "cuda" or "cpu" with `torch.cuda.is_available()`, so on this GPU node Whisper will run on the RTX 6000.

### 4.2. On CPU (for debugging)

On any CPU node or login shell:

```bash
module load conda
conda activate breathwork-py310

cd /gs/home/<your-username>/breathwork-transcription


python pipeline/run_pipeline.py --input "input_file_path"
```

Here `torch.cuda.is_available()` is `False`, so the same code runs on CPU.
