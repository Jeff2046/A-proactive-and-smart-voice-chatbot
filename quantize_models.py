#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用OpenVINO量化压缩模型脚本

该脚本用于量化压缩ASR、TTS、情绪识别和LLM模型，
将模型转换为OpenVINO IR格式并进行量化，以提高推理性能和降低内存占用。
"""

import os
import sys
import logging
from pathlib import Path
from openvino.tools.pot import compress_model_weights
from openvino.tools.ovc import convert_model

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def quantize_model(model_path, output_dir, precision="FP16"):
    """
    量化单个模型
    
    Args:
        model_path: 原始模型路径
        output_dir: 输出目录
        precision: 量化精度，可选FP16、INT8等
    
    Returns:
        量化后的模型路径
    """
    try:
        logger.info(f"开始量化模型: {model_path}")
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取模型文件名
        model_name = Path(model_path).stem
        
        # 转换模型为OpenVINO IR格式
        ir_model = convert_model(model_path)
        
        # 保存原始IR模型
        ir_xml_path = os.path.join(output_dir, f"{model_name}_original.xml")
        ir_bin_path = os.path.join(output_dir, f"{model_name}_original.bin")
        
        # 使用OpenVINO的serialize函数保存模型
        from openvino.runtime import serialize
        serialize(ir_model, ir_xml_path, ir_bin_path)
        
        logger.info(f"已将模型转换为IR格式: {ir_xml_path}")
        
        # 量化模型权重
        quantized_model = compress_model_weights(ir_model, precision=precision)
        
        # 保存量化后的模型
        quantized_xml_path = os.path.join(output_dir, f"{model_name}_{precision.lower()}.xml")
        quantized_bin_path = os.path.join(output_dir, f"{model_name}_{precision.lower()}.bin")
        
        serialize(quantized_model, quantized_xml_path, quantized_bin_path)
        
        logger.info(f"已量化模型并保存: {quantized_xml_path}")
        
        return quantized_xml_path
        
    except Exception as e:
        logger.error(f"量化模型出错: {e}", exc_info=True)
        return None

def main():
    """
    主函数
    """
    logger.info("开始量化所有模型...")
    
    # 模型配置
    models_config = {
        "emotion_detection": {
            "source_path": "models/source/emotion_detection.onnx",  # 原始模型路径
            "output_dir": "models/quantized",
            "precision": "FP16"
        },
        "asr": {
            "source_path": "models/source/asr.onnx",
            "output_dir": "models/quantized",
            "precision": "FP16"
        },
        "tts": {
            "source_path": "models/source/tts.onnx",
            "output_dir": "models/quantized",
            "precision": "FP16"
        },
        "llm": {
            "source_path": "models/source/llm.onnx",
            "output_dir": "models/quantized",
            "precision": "FP16"
        }
    }
    
    # 检查source目录是否存在
    source_dir = "models/source"
    if not os.path.exists(source_dir):
        logger.warning(f"模型源目录不存在: {source_dir}")
        logger.info("请将原始模型文件放入models/source目录后再运行此脚本")
        logger.info("示例模型文件:")
        for model_name, config in models_config.items():
            logger.info(f"  - {config['source_path']}")
        return
    
    # 量化所有模型
    for model_name, config in models_config.items():
        if os.path.exists(config['source_path']):
            quantize_model(
                config['source_path'],
                config['output_dir'],
                config['precision']
            )
        else:
            logger.warning(f"模型文件不存在: {config['source_path']}")
    
    logger.info("所有模型量化完成！")
    logger.info(f"量化后的模型保存在: models/quantized")

if __name__ == "__main__":
    main()
