# 使用官方的 Python 3.11 镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装必要的系统依赖，包括 MySQL 开发库和头文件
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    python-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装 PDM
RUN pip install --no-cache-dir pdm

# 将 PDM 二进制文件添加到 PATH 环境变量
ENV PATH="/root/.local/bin:$PATH"

# 复制 pyproject.toml 和 pdm.lock 文件到工作目录
COPY pyproject.toml pdm.lock ./

# 安装项目依赖
RUN pdm install --prod --no-lock --no-editable

# 复制应用程序代码到工作目录
COPY . .

# 暴露应用程序运行的端口（根据实际需要调整）
EXPOSE 5000

# 设置环境变量以防止 Python 写入缓存
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# 运行应用程序
CMD ["pdm", "run", "python", "manager.py", "runserver"]