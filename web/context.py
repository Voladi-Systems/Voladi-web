from wagtail.models import Locale


def general(request):
    return {
        'LANGUAGES': Locale.objects.all(),
    }


def styles(request):
    context = {
        'h1': 'text-3xl lg:text-4xl font-lato',
        'h2': 'text-2xl lg:text-3xl font-lato',
        'h3': 'text-xl lg:text-2xl font-lato',
        'h4': 'text-lg lg:text-xl font-lato',
        'h5': 'text-md lg:text-lg font-bold font-lato',
        'h6': 'lg:text-md font-bold font-lato',
        'title': 'lg:text-lg font-lato',
        'p': 'lg:text-md',
        'sub_title': 'lg:text-md font-medium',
        'section_padding': 'py-8 md:py-16 xl:py-32',
        'heading_divider_padding': 'py-8 md:py-16',
    }

    return context
