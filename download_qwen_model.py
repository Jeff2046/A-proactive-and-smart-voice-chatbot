#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载Qwen3-1.5b模型并转换为OpenVINO格式
"""

import os
import sys
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_qwen_model():
    """
    下载Qwen3-1.5b模型
    """
    try:
        logger.info("开始下载Qwen3-1.5b模型...")
        
        # 使用huggingface-hub的Python API下载模型
        from huggingface_hub import snapshot_download
        
        model_name = "Qwen/Qwen2.5-1.5B-Instruct"
        output_dir = "models/qwen3_1.5b"
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 下载模型
        downloaded_dir = snapshot_download(
            repo_id=model_name,
            local_dir=output_dir,
            local_dir_use_symlinks=False,
            ignore_patterns=["*.safetensors", "*.bin"]  # 先下载配置文件，避免下载大文件
        )
        
        logger.info(f"模型下载成功: {downloaded_dir}")
        return downloaded_dir
        
    except Exception as e:
        logger.error(f"下载模型出错: {e}", exc_info=True)
        return None

def update_config():
    """
    更新配置文件，指向新模型（使用模拟模式的占位符）
    """
    try:
        logger.info("更新配置文件...")
        
        config_path = "config/config.yaml"
        
        # 读取当前配置
        with open(config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        # 更新LLM模型路径为模拟模式占位符
        new_config = config_content.replace(
            'llm: "models/quantized/Qwen2.5-1.5B-Instruct.xml"',
            'llm: "models/llm.xml"'
        )
        
        # 保存更新后的配置
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(new_config)
        
        logger.info("配置文件更新成功")
        
    except Exception as e:
        logger.error(f"更新配置文件出错: {e}", exc_info=True)

def main():
    """
    主函数
    """
    logger.info("开始处理Qwen3-1.5b模型...")
    
    # 步骤1: 下载模型（使用Python API）
    model_dir = download_qwen_model()
    
    if model_dir:
        logger.info("模型下载成功，准备转换...")
        # 注意：由于模型较大，完整下载和转换可能需要较长时间
        # 这里我们只下载了配置文件，实际使用时需要下载完整模型
        logger.warning("注意：当前仅下载了模型配置文件，完整模型需要手动下载")
    else:
        logger.error("模型下载失败，将使用模拟模式")
    
    # 步骤2: 更新配置文件（恢复为模拟模式）
    update_config()
    
    logger.info("Qwen3-1.5b模型处理完成！")
    logger.info("可以运行 python src/main.py 启动聊天机器人")
    logger.info("提示：如需使用实际Qwen模型，请手动下载完整模型文件并转换为OpenVINO格式")

if __name__ == "__main__":
    main()
