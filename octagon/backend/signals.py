# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AIModel
from django.conf import settings
from .compilemodel import compile_prover
import asyncio
import os
import torch

@receiver(post_save, sender=AIModel)
def execute_after_model_save(sender, instance, created, **kwargs):
    if created:
        # Your function logic here
        print(f"AIModel instance created: {instance.name}")
        # Call any other function here
        my_custom_function(instance)

def my_custom_function(instance):
    media_root = settings.MEDIA_ROOT
    file_path = os.path.join(media_root, instance.file.name)
    file_path = file_path.replace('/model.onnx', '')

    # Define what you want to do with the instance
    print(f"Executing compiling AIModel: {file_path}")
    x = torch.tensor([[[0.8790, 0.6273, 0.2377, 0.5785, 0.9947, 0.9937, 0.5818, 0.6087,
          0.6087, 0.6312]]])

    res = asyncio.run(compile_prover(file_path, x.shape))
    print(res)