#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用huggingface-hub下载Qwen2.5-1.5B-Instruct模型
"""

import os
import logging
from huggingface_hub import snapshot_download

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    logger.info("开始下载Qwen2.5-1.5B-Instruct模型...")
    
    # 模型信息
    model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    local_dir = "models/qwen3_1.5b"
    
    # 确保本地目录存在
    os.makedirs(local_dir, exist_ok=True)
    
    try:
        # 下载模型
        logger.info(f"正在从Hugging Face下载模型: {model_id}")
        logger.info(f"保存到本地目录: {local_dir}")
        
        # 使用snapshot_download下载模型
        downloaded_dir = snapshot_download(
            repo_id=model_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            # 下载完整模型，包括权重文件
            allow_patterns=["*.json", "*.model", "tokenizer*", "generation_config*", "*.safetensors"]
            # 移除了对权重文件的限制
        )
        
        logger.info(f"模型下载成功！保存目录: {downloaded_dir}")
        logger.info("注意：当前仅下载了配置文件，如需完整模型，请移除ignore_patterns中的限制")
        
    except Exception as e:
        logger.error(f"模型下载失败: {e}", exc_info=True)

if __name__ == "__main__":
    main()
