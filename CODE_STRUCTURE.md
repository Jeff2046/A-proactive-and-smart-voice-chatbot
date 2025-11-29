# 高情商聊天机器人 - 代码结构与使用指南

## 1. 项目概述

本项目是一个基于OpenVINO-GenAI的高情商聊天机器人，具备视频情绪识别、双工对话、主动关心、吃药提醒和天气汇报等功能。完全基于本地运行，断网可用。

## 2. 详细代码结构

### 2.1 核心模块关系

```
┌─────────────────────────────────────────────────────────────────┐
│                          main.py                                │
│                     （程序入口）                                 │
└───────────────┬─────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────┐
│                        chatbot.py                               │
│                     （聊天机器人核心）                           │
├───────────────┬───────────────┬───────────────┬───────────────┤
│ emotion_recog │     asr.py     │     tts.py     │     llm.py    │
│ nition.py     │ （语音识别）   │ （文本转语音） │ （大语言模型） │
└───────────────┴───────────────┴───────────────┴───────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                          weather.py                             │
│                     （天气信息模块）                             │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 模块详细说明

#### 2.2.1 main.py - 程序入口

**功能**：初始化聊天机器人并启动主循环

**核心代码**：
```python
from src.chatbot import EmotionalChatbot
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("正在启动高情商聊天机器人...")
    chatbot = EmotionalChatbot()
    chatbot.start()

if __name__ == "__main__":
    main()
```

**执行流程**：
1. 配置日志
2. 创建EmotionalChatbot实例
3. 调用start()方法启动聊天机器人

#### 2.2.2 chatbot.py - 聊天机器人核心

**功能**：协调各个模块，处理对话逻辑，实现主动对话

**核心类**：`EmotionalChatbot`

**主要方法**：
- `__init__()`: 初始化各个模块
- `start()`: 启动聊天机器人
- `_run_emotion_recognition()`: 情绪识别线程，每5秒检测一次情绪，每2分钟分析一次
- `_trigger_active_conversation()`: 触发主动对话
- `_handle_user_input()`: 处理用户输入
- `_generate_response()`: 生成机器人响应

**情绪检测逻辑**：
```python
# 情绪检测计数器
detection_count = 0
# 每2分钟分析一次（24次检测 × 5秒 = 120秒）
analysis_interval = 24
while self.is_running:
    emotion = self.emotion_recognizer.recognize_emotion()
    detection_count += 1
    self.logger.info(f"情绪检测 #{detection_count}: {emotion}")
    if detection_count >= analysis_interval:
        self.logger.info(f"每2分钟情绪分析: {emotion}")
        if emotion in self.config['emotion']['abnormal_emotions']:
            self._trigger_active_conversation(f"检测到您情绪{emotion}，需要聊聊天吗？")
        detection_count = 0
    time.sleep(5)
```

#### 2.2.3 emotion_recognition.py - 情绪识别模块

**功能**：通过摄像头实时识别用户情绪

**核心类**：`EmotionRecognizer`

**主要方法**：
- `__init__()`: 初始化情绪识别模型和摄像头
- `recognize_emotion()`: 识别情绪，返回情绪标签
- `_init_camera()`: 初始化摄像头
- `_load_model()`: 加载情绪识别模型

**摄像头初始化**：
```python
def _init_camera(self):
    """初始化摄像头"""
    self.logger.info("正在尝试打开摄像头...")
    self.cap = cv2.VideoCapture(0)
    if self.cap.isOpened():
        self.logger.info("摄像头已成功打开")
        # 设置摄像头参数
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camera_available = True
    else:
        self.logger.error("无法打开摄像头")
        self.camera_available = False
```

**情绪识别流程**：
1. 从摄像头读取帧
2. 预处理图像
3. 使用模型预测情绪
4. 返回情绪结果
5. 如无模型，使用模拟情绪

#### 2.2.4 asr.py - 语音识别模块

**功能**：将用户语音转换为文本

**核心类**：`ASR`

**主要方法**：
- `__init__()`: 初始化语音识别器
- `recognize_speech()`: 识别语音，返回文本

**语音识别流程**：
1. 使用SpeechRecognition库监听麦克风
2. 调用Google语音识别API（可替换为本地模型）
3. 返回识别结果

#### 2.2.5 tts.py - 文本转语音模块

**功能**：将文本转换为语音并播放

**核心类**：`TTS`

**主要方法**：
- `__init__()`: 初始化TTS引擎
- `speak()`: 将文本转换为语音并播放

**语音播放优化**：
使用系统临时目录存储音频文件，解决权限问题：
```python
def speak(self, text):
    """将文本转换为语音并播放"""
    try:
        # 使用系统临时目录创建临时音频文件
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_audio_path = temp_file.name
        
        # 生成语音文件
        tts = gTTS(text=text, lang='zh-CN')
        tts.save(temp_audio_path)
        
        # 播放语音
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_path)
        pygame.mixer.music.play()
        
        # 等待播放完成
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        # 清理资源
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.unlink(temp_audio_path)
        
        self.logger.info(f"TTS播放完成: {text}")
    except Exception as e:
        self.logger.error(f"TTS播放失败: {e}")
```

#### 2.2.6 llm.py - 大语言模型模块

**功能**：生成机器人响应，结合情绪信息

**核心类**：`LLM`

**主要方法**：
- `__init__()`: 初始化LLM模型
- `generate_response()`: 生成响应

**模拟模式**：当没有实际模型时，根据情绪生成模拟响应

#### 2.2.7 weather.py - 天气模块

**功能**：提供本地天气信息

**核心类**：`Weather`

**主要方法**：
- `__init__()`: 初始化天气数据
- `get_weather()`: 获取天气信息

**本地天气数据**：使用本地JSON文件存储天气数据，支持离线使用

## 3. 配置文件详解

### 3.1 config.yaml - 主配置文件

```yaml
# OpenVINO配置
openvino:
  device: "CPU"  # 可以是CPU, GPU, MYRIAD等
  precision: "FP16"  # 模型精度

# 模型路径配置
models:
  emotion_detection: "models/emotion-detection-retail-0003.xml"
  asr: "models/asr_model.xml"
  tts: "models/tts_model.xml"
  llm: "models/llm.xml"

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

### 3.2 配置项说明

| 配置项 | 说明 | 示例值 |
|--------|------|--------|
| openvino.device | 运行设备 | CPU, GPU, MYRIAD |
| openvino.precision | 模型精度 | FP16, INT8 |
| models.emotion_detection | 情绪检测模型路径 | models/emotion-detection-retail-0003.xml |
| emotion.threshold | 异常情绪检测阈值 | 0.7 |
| emotion.abnormal_emotions | 需要关注的异常情绪 | ["angry", "sad", "fear"] |
| reminders.medication_times | 吃药提醒时间 | ["08:00", "12:00", "18:00"] |
| weather.location | 默认天气查询位置 | 北京 |
| weather.update_time | 每日天气汇报时间 | 07:00 |

## 4. 运行流程

### 4.1 启动流程

```
1. 启动main.py
2. 初始化EmotionalChatbot
   - 初始化情绪识别模块
   - 初始化ASR模块
   - 初始化TTS模块
   - 初始化LLM模块
   - 初始化天气模块
3. 启动情绪识别线程
4. 设置定时任务
5. 进入对话循环
   - 等待用户语音输入
   - 识别语音
   - 生成响应
   - 播放响应
   - 继续等待用户输入
```

### 4.2 情绪识别流程

```
1. 情绪识别线程启动
2. 每5秒检测一次情绪
3. 每24次检测（120秒）分析一次情绪
4. 如果检测到异常情绪，触发主动对话
5. 继续循环
```

### 4.3 对话流程

```
1. 等待用户语音输入
2. 识别用户语音
3. 生成机器人响应
4. 播放机器人响应
5. 继续等待用户输入
6. 支持用户打断机器人说话
```

## 5. 使用方法

### 5.1 安装依赖

```bash
pip install -r requirements.txt
```

### 5.2 配置模型

1. 下载模型文件
   - 情绪识别模型：emotion-detection-retail-0003
   - ASR模型：根据需要选择
   - TTS模型：根据需要选择
   - LLM模型：通用千问多模态模型

2. 量化模型
   ```bash
   python quantize_models.py
   ```

### 5.3 启动聊天机器人

```bash
python src/main.py
```

### 5.4 交互方式

1. **语音输入**：直接对着麦克风说话
2. **打断机器人**：在机器人说话时，可以直接说话打断
3. **主动对话**：机器人会在以下情况主动发起对话：
   - 检测到异常情绪
   - 到达吃药提醒时间
   - 天气更新时间

## 6. 模拟模式

当没有实际模型文件时，系统会自动切换到模拟模式：

- **情绪识别**：随机生成情绪
- **LLM响应**：根据情绪生成模拟响应
- **天气信息**：使用本地默认数据

## 7. 模型下载与量化

### 7.1 下载模型

使用提供的下载脚本：

```bash
# 下载千问模型
python download_qwen_model.py

# 下载其他模型
python download_models.py
```

### 7.2 模型转换与量化

1. 转换为ONNX格式
   ```bash
   python convert_qwen_to_onnx.py
   ```

2. 使用OpenVINO量化
   ```bash
   python quantize_models.py
   ```

## 8. 调试与故障排除

### 8.1 日志查看

日志文件保存在`logs/chatbot.log`，可以查看系统运行状态和错误信息：

```bash
tail -f logs/chatbot.log
```

### 8.2 常见问题

1. **摄像头无法打开**
   - 检查摄像头是否被其他程序占用
   - 检查摄像头权限
   - 尝试更换摄像头设备索引

2. **语音识别失败**
   - 检查麦克风是否正常工作
   - 检查网络连接（如果使用在线API）
   - 尝试提高音量

3. **TTS播放失败**
   - 检查音频设备是否正常
   - 检查Pygame库是否正确安装

4. **模型加载失败**
   - 检查模型文件路径是否正确
   - 检查模型文件是否完整
   - 检查OpenVINO版本是否兼容

## 9. 扩展开发

### 9.1 添加新的情绪类型

1. 在配置文件中添加新的情绪类型
2. 修改情绪识别模型或模拟逻辑
3. 在LLM响应生成中添加新情绪的处理

### 9.2 更换语音识别引擎

修改`asr.py`中的`recognize_speech()`方法，替换为其他语音识别引擎。

### 9.3 更换文本转语音引擎

修改`tts.py`中的`speak()`方法，替换为其他TTS引擎。

### 9.4 添加新的主动对话类型

在`chatbot.py`中添加新的触发条件和对话逻辑。

## 10. 性能优化

1. **模型量化**：使用INT8精度量化模型，提高推理速度
2. **多线程优化**：确保各个模块在独立线程中运行，避免阻塞
3. **资源管理**：及时释放摄像头、音频设备等资源
4. **日志级别**：在生产环境中降低日志级别，减少IO开销

## 11. 安全考虑

1. **本地运行**：所有数据都在本地处理，保护用户隐私
2. **模型安全**：使用经过验证的模型，避免恶意模型
3. **权限控制**：仅请求必要的权限（摄像头、麦克风）
4. **数据保护**：不存储用户语音数据和对话内容

## 12. 未来改进方向

- 支持更多情绪类型
- 优化语音识别准确率
- 支持更多本地大模型
- 添加可视化界面
- 支持多语言
- 优化模型推理速度
- 添加更多主动对话场景

## 13. 许可证

MIT License

## 14. 贡献指南

欢迎提交Issue和Pull Request，共同改进这个项目。

## 15. 联系方式

如有问题或建议，欢迎联系项目维护者。
