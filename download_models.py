#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载和部署实际模型文件脚本

使用OpenVINO Model Downloader下载所需的模型文件，并部署到models目录。
"""

import os
import sys
import logging
import subprocess
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_model_with_omz(model_name, output_dir):
    """
    使用OpenVINO Model Downloader下载模型
    
    Args:
        model_name: 模型名称
        output_dir: 输出目录
    """
    try:
        logger.info(f"使用OMZ下载模型: {model_name}")
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 构建命令
        cmd = [
            "omz_downloader",
            "--name", model_name,
            "--output_dir", output_dir,
            "--precision", "FP16"
        ]
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(f"OMZ下载输出: {result.stdout}")
        
        if result.stderr:
            logger.warning(f"OMZ下载警告: {result.stderr}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"OMZ下载失败: {e}")
        logger.error(f"命令输出: {e.output}")
        return False
    except Exception as e:
        logger.error(f"下载模型出错: {e}", exc_info=True)
        return False

def copy_model_files(model_name, source_dir, target_dir):
    """
    将下载的模型文件复制到目标目录
    
    Args:
        model_name: 模型名称
        source_dir: 源目录
        target_dir: 目标目录
    """
    try:
        logger.info(f"复制模型文件: {model_name}")
        
        # 查找模型文件
        model_files = {
            "xml": list(Path(source_dir).rglob(f"{model_name}*.xml")),
            "bin": list(Path(source_dir).rglob(f"{model_name}*.bin"))
        }
        
        if not model_files["xml"] or not model_files["bin"]:
            logger.error(f"未找到模型文件: {model_name}")
            return False
        
        # 复制文件
        for ext, files in model_files.items():
            if files:
                src_file = files[0]
                dst_file = os.path.join(target_dir, f"{model_name}.{ext}")
                
                # 使用subprocess复制文件（兼容Windows和Linux）
                if sys.platform == "win32":
                    cmd = ["copy", str(src_file), str(dst_file), "/Y"]
                else:
                    cmd = ["cp", str(src_file), str(dst_file)]
                
                subprocess.run(cmd, check=True, shell=sys.platform == "win32")
                logger.info(f"已复制: {src_file} -> {dst_file}")
        
        return True
        
    except Exception as e:
        logger.error(f"复制模型文件出错: {e}", exc_info=True)
        return False

def main():
    """
    主函数
    """
    logger.info("开始下载和部署模型文件...")
    
    # 模型配置
    models = [
        "emotion-detection-retail-0003",
        "quartznet-15x5-en",
        "text-to-speech-en-0001"
    ]
    
    # 临时下载目录
    temp_dir = "models_temp"
    
    # 目标目录
    target_dir = "models"
    
    # 下载并复制所有模型
    for model_name in models:
        logger.info(f"\n处理模型: {model_name}")
        
        # 下载模型
        if download_model_with_omz(model_name, temp_dir):
            # 复制模型文件
            copy_model_files(model_name, temp_dir, target_dir)
    
    # 清理临时目录
    if os.path.exists(temp_dir):
        try:
            if sys.platform == "win32":
                subprocess.run(["rmdir", "/S", "/Q", temp_dir], check=True, shell=True)
            else:
                subprocess.run(["rm", "-rf", temp_dir], check=True)
            logger.info(f"已清理临时目录: {temp_dir}")
        except Exception as e:
            logger.warning(f"清理临时目录失败: {e}")
    
    # 提示LLM模型需要手动处理
    logger.info("\n注意：")
    logger.info("1. LLM模型（通用千问多模态大模型）较大，建议手动下载或使用本地模型")
    logger.info("2. 请将LLM模型文件（llm.xml和llm.bin）放入models目录")
    logger.info("3. 如需使用其他模型，请更新config/config.yaml中的模型路径配置")
    
    logger.info("\n模型下载和部署完成！")
    logger.info("可以运行 python src/main.py 启动聊天机器人")

if __name__ == "__main__":
    main()
