#!/bin/bash
# Export model for production deployment
# Supports TorchScript, ONNX, and Whisper.cpp quantization

set -e

# Configuration
MODEL_PATH=""
OUTPUT_DIR="./exported"
OUTPUT_FORMAT="torchscript"  # torchscript, onnx, whisper_cpp
QUANTIZE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --model_path)
            MODEL_PATH="$2"
            shift 2
            ;;
        --output_dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --output_format)
            OUTPUT_FORMAT="$2"
            shift 2
            ;;
        --quantize)
            QUANTIZE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate inputs
if [ -z "$MODEL_PATH" ]; then
    echo "Error: --model_path is required"
    echo "Usage: ./export_model.sh --model_path <path> [--output_dir <dir>] [--output_format <format>] [--quantize]"
    exit 1
fi

echo "========================================"
echo "Model Export Script"
echo "========================================"
echo "Model path: $MODEL_PATH"
echo "Output directory: $OUTPUT_DIR"
echo "Output format: $OUTPUT_FORMAT"
echo "Quantization: $QUANTIZE"
echo "========================================"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Export based on format
case $OUTPUT_FORMAT in
    torchscript)
        echo "Exporting to TorchScript..."
        python3 <<EOF
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Load model
print("Loading model...")
model = Wav2Vec2ForCTC.from_pretrained("$MODEL_PATH")
processor = Wav2Vec2Processor.from_pretrained("$MODEL_PATH")

# Set to eval mode
model.eval()

# Create dummy input
dummy_input = torch.randn(1, 16000)
inputs = processor(dummy_input, sampling_rate=16000, return_tensors="pt")

# Trace model
print("Tracing model...")
traced_model = torch.jit.trace(model, inputs.input_values)

# Save
output_path = "$OUTPUT_DIR/model.pt"
torch.jit.save(traced_model, output_path)
print(f"✓ Saved TorchScript model to {output_path}")

# Save processor
processor.save_pretrained("$OUTPUT_DIR")
print(f"✓ Saved processor to $OUTPUT_DIR")
EOF
        ;;
    
    onnx)
        echo "Exporting to ONNX..."
        python3 <<EOF
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from optimum.onnxruntime import ORTModelForCTC

# Load model
print("Loading model...")
model = Wav2Vec2ForCTC.from_pretrained("$MODEL_PATH")
processor = Wav2Vec2Processor.from_pretrained("$MODEL_PATH")

# Export to ONNX
print("Converting to ONNX...")
ort_model = ORTModelForCTC.from_pretrained("$MODEL_PATH", export=True)

# Save
ort_model.save_pretrained("$OUTPUT_DIR")
processor.save_pretrained("$OUTPUT_DIR")

print(f"✓ Saved ONNX model to $OUTPUT_DIR")

# Optionally quantize
if $QUANTIZE; then
    print("Quantizing ONNX model...")
    from onnxruntime.quantization import quantize_dynamic, QuantType
    
    quantize_dynamic(
        "$OUTPUT_DIR/model.onnx",
        "$OUTPUT_DIR/model_quantized.onnx",
        weight_type=QuantType.QUInt8
    )
    print(f"✓ Saved quantized model to $OUTPUT_DIR/model_quantized.onnx")
EOF
        ;;
    
    whisper_cpp)
        echo "Exporting for whisper.cpp..."
        echo "Note: This requires whisper.cpp to be installed"
        echo "See: https://github.com/ggerganov/whisper.cpp"
        
        # Check if whisper.cpp is available
        if [ ! -d "whisper.cpp" ]; then
            echo "Cloning whisper.cpp..."
            git clone https://github.com/ggerganov/whisper.cpp.git
            cd whisper.cpp
            make
            cd ..
        fi
        
        echo "Converting model to whisper.cpp format..."
        python3 whisper.cpp/models/convert-h5-to-ggml.py "$MODEL_PATH" "$OUTPUT_DIR" whisper
        
        if $QUANTIZE; then
            echo "Quantizing for whisper.cpp..."
            ./whisper.cpp/quantize "$OUTPUT_DIR/ggml-model.bin" "$OUTPUT_DIR/ggml-model-q8_0.bin" q8_0
            echo "✓ Quantized model saved to $OUTPUT_DIR/ggml-model-q8_0.bin"
        fi
        ;;
    
    *)
        echo "Error: Unknown format $OUTPUT_FORMAT"
        echo "Supported formats: torchscript, onnx, whisper_cpp"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "✓ Export complete!"
echo "Output: $OUTPUT_DIR"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Test exported model"
echo "  2. Benchmark inference speed"
echo "  3. Deploy to production"
echo ""
