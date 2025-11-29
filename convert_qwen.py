#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Qwen模型转换为OpenVINO格式
"""

import os
import logging
import subprocess

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    logger.info("开始将Qwen模型转换为OpenVINO格式...")
    
    # 模型信息
    model_dir = "models/qwen3_1.5b"
    output_dir = "models/quantized"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 转换命令
        output_model = os.path.join(output_dir, "qwen3_1.5b.xml")
        
        cmd = [
            "ovc",
            model_dir,
            "--output_model", output_model,
            "--compress_to_fp16"
        ]
        
        logger.info(f"执行转换命令: {' '.join(cmd)}")
        
        # 执行转换
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        logger.info(f"转换成功！输出: {result.stdout}")
        
        if result.stderr:
            logger.warning(f"转换警告: {result.stderr}")
        
        logger.info(f"转换后的模型保存在: {output_model}")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"转换失败: {e}")
        logger.error(f"命令输出: {e.output}")
        logger.error(f"错误信息: {e.stderr}")
    except Exception as e:
        logger.error(f"转换过程中出错: {e}", exc_info=True)

if __name__ == "__main__":
    main()
