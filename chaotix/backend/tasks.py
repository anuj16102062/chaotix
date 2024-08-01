import boto3
import requests
from celery import shared_task
from django.conf import settings
from .models import GeneratedImage
from io import BytesIO
import os

@shared_task
def generate_image_and_save(prompt):
    api_url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
    headers = {
        "authorization": f"Bearer {settings.STABILITY_API_KEY}",
        "accept": "image/*"
    }
    try:
        response = requests.post(
            api_url,
            headers=headers,
            files={"none": ''},
            data={
                "prompt": prompt,
                "output_format": "jpeg",
            }
        )
        if response.status_code == 200:
            image_content = BytesIO(response.content)
            file_name = f"{prompt.replace(' ', '_')}.jpeg"
            local_file_path = os.path.join(settings.MEDIA_ROOT, file_name) #stored locally for reference purpose
            with open(local_file_path, 'wb') as file:
                file.write(image_content.getvalue())
            s3 = boto3.client('s3')
            s3.upload_file(local_file_path, settings.AWS_STORAGE_BUCKET_NAME, file_name)
            image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}"
            # print(image_url, '-------------image_url--25')
            GeneratedImage.objects.create(url=image_url, metadata={'prompt': prompt})
            return image_url
        else:
            return f"Error generating image: {response.json()}"
    except Exception as e:
        return f"Exception: {str(e)}"
