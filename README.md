# 高情商聊天机器人

基于OpenVINO-GenAI的双工可主动对话的高情商聊天机器人，通过视频识别情绪，支持异常情绪主动聊天、吃药提醒、每日天气汇报等功能。

## 功能特性

- 🎥 **视频情绪识别**：实时识别用户情绪，根据情绪调整对话策略
- 💬 **双工对话**：支持用户在机器人说话时打断，实现自然流畅的对话
- 🗣️ **主动对话**：
  - 检测到异常情绪时主动关心
  - 定时吃药提醒
  - 每日天气汇报
- 🔊 **语音交互**：支持语音输入和语音输出
- 🧠 **多模态大模型**：集成通用千问多模态大模型
- 📱 **本地运行**：完全基于本地，断网可用
- ⚡ **高效推理**：使用OpenVINO量化压缩模型，提高推理性能

## 技术栈

- **框架**：OpenVINO-GenAI
- **语言**：Python 3.8+
- **计算机视觉**：OpenCV
- **语音识别**：SpeechRecognition
- **文本转语音**：gTTS + Pygame
- **大语言模型**：通用千问多模态模型
- **模型优化**：OpenVINO量化压缩

## 项目结构

```
├── config/              # 配置文件目录
│   └── config.yaml      # 主配置文件
├── data/                # 数据目录
│   └── weather_data.json # 本地天气数据
├── logs/                # 日志目录
├── models/              # 模型目录
│   ├── source/          # 原始模型文件
│   └── quantized/       # 量化后的模型文件
├── src/                 # 源代码目录
│   ├── chatbot.py       # 聊天机器人核心类
│   ├── emotion_recognition.py # 情绪识别模块
│   ├── asr.py           # 语音识别模块
│   ├── tts.py           # 文本转语音模块
│   ├── llm.py           # 大语言模型模块
│   └── weather.py       # 天气模块
├── main.py              # 主入口文件
├── quantize_models.py   # 模型量化脚本
├── requirements.txt     # 依赖包列表
└── README.md            # 项目说明文档
```

## 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置模型

- 将原始模型文件放入 `models/source/` 目录
- 支持的模型格式：ONNX
- 运行模型量化脚本：

```bash
python quantize_models.py
```

### 3. 配置参数

编辑 `config/config.yaml` 文件，根据需要调整配置：

```yaml
# OpenVINO配置
openvino:
  device: "CPU"  # 可以是CPU, GPU, MYRIAD等
  precision: "FP16"  # 模型精度

# 模型路径配置
models:
  emotion_detection: "models/quantized/emotion_detection_fp16.xml"
  asr: "models/quantized/asr_fp16.xml"
  tts: "models/quantized/tts_fp16.xml"
  llm: "models/quantized/llm_fp16.xml"

# 情绪识别配置
emotion:
  threshold: 0.7  # 异常情绪检测阈值
  abnormal_emotions: ["angry", "sad", "fear"]  # 需要关注的异常情绪

# 提醒配置
reminders:
  medication_times: ["08:00", "12:00", "18:00"]  # 吃药提醒时间

# 天气配置
weather:
  location: "北京"  # 默认天气查询位置
  update_time: "07:00"  # 每日天气汇报时间
```

## 使用方法

### 启动聊天机器人

```bash
python src/main.py
```

### 交互方式

1. **语音输入**：直接对着麦克风说话，机器人会自动识别
2. **打断机器人**：在机器人说话时，可以直接说话打断它
3. **主动对话**：机器人会在检测到异常情绪、到达吃药时间或天气更新时间时主动发起对话

## 模拟模式

当没有实际模型文件时，系统会自动切换到模拟模式：
- 情绪识别：随机生成情绪
- LLM响应：根据情绪生成模拟响应
- 天气信息：使用本地默认数据

## 模型量化

使用OpenVINO量化压缩模型，支持多种精度：
- FP16：平衡性能和精度
- INT8：更高性能，更低内存占用

运行量化脚本：

```bash
python quantize_models.py
```

## 日志

日志文件保存在 `logs/chatbot.log`，可以查看系统运行状态和错误信息。

## 注意事项

1. **摄像头权限**：确保程序有访问摄像头的权限
2. **麦克风权限**：确保程序有访问麦克风的权限
3. **模型文件**：首次运行需要准备模型文件，或使用模拟模式
4. **网络连接**：模拟模式下无需网络，实际模型需要提前下载

## 未来改进

- [ ] 支持更多情绪类型
- [ ] 优化语音识别准确率
- [ ] 支持更多本地大模型
- [ ] 添加可视化界面
- [ ] 支持多语言

## 许可证

MIT License
