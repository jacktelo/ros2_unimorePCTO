ARG FROM_IMAGE=ubuntu:22.04
FROM $FROM_IMAGE

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble
ENV COLCON_WS=ws

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    wget curl gnupg2 rsync git \
    lsb-release lsb-core unzip \
    python3 python3-pip python3-yaml python3-tk python3-venv \
    build-essential cmake \
    vim bash-completion htop net-tools \
    && rm -rf /var/lib/apt/lists/*

# Install ROS2 Humble
RUN apt update && apt install -y locales && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

RUN apt install -y software-properties-common && \
    add-apt-repository universe && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN apt update && apt install -y \
    ros-${ROS_DISTRO}-ros-base \
    ros-${ROS_DISTRO}-cv-bridge \
    ros-${ROS_DISTRO}-sensor-msgs \
    ros-${ROS_DISTRO}-geometry-msgs \
    ros-${ROS_DISTRO}-message-filters \
    ros-${ROS_DISTRO}-realsense2-camera \
    python3-argcomplete \
    python3-colcon-common-extensions \
    python3-vcstool \
    ros-dev-tools \
    && rm -rf /var/lib/apt/lists/*

# Install vision dependencies  
RUN apt-get update && apt-get install -y \
    libglfw3-dev libglfw3 libassimp-dev \
    python-is-python3 \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -d /home/vscode vscode && \
    echo vscode:vscode | chpasswd && \
    usermod -aG sudo vscode && \
    usermod --shell /bin/bash vscode && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN mkdir -p /pcto/${COLCON_WS}/src && \
    chown -R vscode:vscode /pcto

USER vscode
WORKDIR /home/vscode

# Source ROS2 in bashrc
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

WORKDIR /pcto