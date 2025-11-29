#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Qwen模型转换为ONNX格式
"""

import os
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    logger.info("开始将Qwen模型转换为ONNX格式...")
    
    # 模型信息
    model_dir = "models/qwen3_1.5b"
    onnx_output = "models/qwen3_1.5b/qwen3_1.5b.onnx"
    
    try:
        # 加载模型
        logger.info(f"加载模型: {model_dir}")
        
        model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        
        logger.info("模型加载成功")
        
        # 准备示例输入
        inputs = tokenizer("你好", return_tensors="pt").to(model.device)
        
        # 导出为ONNX
        logger.info(f"导出为ONNX格式: {onnx_output}")
        
        torch.onnx.export(
            model,
            tuple(inputs.values()),
            onnx_output,
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=['input_ids', 'attention_mask'],
            output_names=['output'],
            dynamic_axes={
                'input_ids': {0: 'batch_size', 1: 'sequence_length'},
                'attention_mask': {0: 'batch_size', 1: 'sequence_length'},
                'output': {0: 'batch_size', 1: 'sequence_length'}
            }
        )
        
        logger.info("ONNX转换成功！")
        
    except Exception as e:
        logger.error(f"转换失败: {e}", exc_info=True)

if __name__ == "__main__":
    main()
