# Model Files

This directory is intended for storing model files or checkpoints.

## Using Pre-trained Models

The LLM Chatbot is designed to work with Hugging Face Transformers models. By default, it will download models from the Hugging Face Hub as needed.

Popular models for chatbots include:

- `gpt2` - OpenAI's GPT-2 model (small version)
- `distilgpt2` - A distilled version of GPT-2, smaller and faster
- `microsoft/DialoGPT-small` - A model fine-tuned for dialogue
- `microsoft/DialoGPT-medium` - A larger dialogue model

## Saving Custom Models

If you fine-tune a model for your specific use case, you can save it to this directory:

```python
# After training your model
model.save_pretrained("./models/my_custom_model")
tokenizer.save_pretrained("./models/my_custom_model")

# To use your custom model
config = Config()
config.model_name = "./models/my_custom_model"
chatbot = Chatbot(config)
```

## Model Size Considerations

Be aware of the memory requirements for different models:

- Small models (GPT-2, DialoGPT-small): ~500MB
- Medium models (GPT-2 Medium, DialoGPT-medium): ~1.5GB
- Large models: 3GB+

For resource-constrained environments, stick with smaller models or consider quantized versions.
