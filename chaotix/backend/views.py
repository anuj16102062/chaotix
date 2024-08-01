from django.shortcuts import render
from .forms import ImageGenerationForm
from .tasks import generate_image_and_save
from .models import GeneratedImage

def generate_images(request):
    if request.method == 'POST':
        form = ImageGenerationForm(request.POST)
        if form.is_valid():
            prompts = [
                form.cleaned_data['text1'],
                form.cleaned_data['text2'],
                form.cleaned_data['text3']
            ]
            results = []
            for prompt in prompts:
                try:
                    result = generate_image_and_save.delay(prompt)
                    results.append(result)
                except Exception as e:
                    return render(request, 'generator/result.html', {
                        'error': str(e),
                        'image_urls': []
                    })

            return render(request, 'generator/result.html', {'results': results})
    else:
        form = ImageGenerationForm()
    image_urls = GeneratedImage.objects.all()

    return render(request, 'generator/generate.html', {'form': form, 'image_urls': image_urls})
