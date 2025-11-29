#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聊天机器人测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import yaml
from pathlib import Path
from src.chatbot import EmotionChatBot

class TestChatBot:
    """聊天机器人测试类"""
    
    def __init__(self):
        """初始化测试"""
        # 加载配置
        config_path = Path(__file__).parent / "config" / "config.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 初始化聊天机器人
        self.chatbot = EmotionChatBot(self.config)
        print("聊天机器人初始化完成")
    
    def test_emotion_recognition(self):
        """测试情绪识别"""
        print("\n=== 测试情绪识别 ===")
        emotion = self.chatbot.emotion_recognizer.recognize_emotion()
        print(f"识别到的情绪: {emotion}")
    
    def test_llm_response(self):
        """测试LLM响应生成"""
        print("\n=== 测试LLM响应生成 ===")
        test_inputs = [
            "你好",
            "今天天气怎么样",
            "我感到很高兴",
            "我很生气"
        ]
        
        for input_text in test_inputs:
            emotion = self.chatbot.emotion_recognizer.recognize_emotion()
            # 构建正确的对话历史格式
            conversation_history = [{"role": "user", "content": input_text}]
            response = self.chatbot.llm.generate_response(
                input_text, 
                conversation_history, 
                emotion,
                image=None
            )
            print(f"用户输入: {input_text}\n情绪: {emotion}\n机器人响应: {response}\n")
    
    def test_weather(self):
        """测试天气获取"""
        print("\n=== 测试天气获取 ===")
        weather_info = self.chatbot.weather.get_weather()
        print(f"天气信息: {weather_info}")
    
    def test_tts(self):
        """测试TTS功能"""
        print("\n=== 测试TTS功能 ===")
        test_text = "这是一个测试，用于验证文本转语音功能是否正常工作。"
        print(f"将文本转换为语音: {test_text}")
        self.chatbot.tts.speak(test_text)
        print("语音播放完成")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始运行聊天机器人测试...")
        self.test_emotion_recognition()
        self.test_llm_response()
        self.test_weather()
        self.test_tts()
        print("\n所有测试运行完成！")

if __name__ == "__main__":
    tester = TestChatBot()
    tester.run_all_tests()
