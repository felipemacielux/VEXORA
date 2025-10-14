# src/theming/context_processors.py
def theme(request):
    return {
        "PLATFORM_NAME": "Vexora",
        "THEME": {
            "primary": "#6356e5",
            "primary_strong": "#3a2ade",
            "primary_soft": "#8c82ec",
            "bg": "#f3f6f6",
            "surface": "#ffffff",
            "text": "#0f172a",
            "muted": "#475569",
            "border": "#e2e8f0",
            "accent": "#8c82ec",
        }
    }
