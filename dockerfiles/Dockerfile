#cd docker && docker build -t itmt -f Dockerfile . 
#docker run --gpus all -it itmt
FROM mhubai/base:latest


# Clone the main branch of MHubAI/models
RUN git stash \
 && git sparse-checkout set "models/DeepSarconia" \
 && git fetch https://github.com/MHubAI/models.git main \
 && git merge FETCH_HEAD

# Clone the DeepSarcopenia model
RUN git clone https://github.com/AIM-KannLab/DeepSarcopenia /app/models/DeepSarcopenia


#FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04
ENV TZ=US/Eastern
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y tzdata

RUN apt update && \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.9 python3-pip python3-setuptools python3-distutils && \
    apt clean && rm -rf /var/lib/apt/lists/*

RUN python3.9 -m pip install --upgrade pip 

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir  tensorflow==2.10 \
    nilearn pandas \
    scipy numpy matplotlib tqdm imageio scikit-image \
    scikit-learn itk-elastix SimpleITK nibabel intensity-normalization[ants]\
    wandb jupyter opencv-python  

RUN python3.9 -c "import tensorflow"

#COPY src /src
#COPY model/test /model/test
#COPY preprocessing /preprocessing
#COPY data data/
#COPY main.py /
#COPY get_CSA.py /
#COPY get_dice.py /
#COPY statistics.py /
#COPY visualize.py /
#COPY opt.py /
ENTRYPOINT ["python3", "-m", "mhubio.run"]
CMD ["--config", "/app/models/DeepSarcopenia/config/default.yml"]
#CMD [ "python3.9", "./main.py" ]