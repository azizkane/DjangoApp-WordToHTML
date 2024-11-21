COLORS = {
    'primary': '#1a73e8',  # Modern Google-style blue
    'secondary': '#202124',
    'accent': '#4285f4',
    'background': '#ffffff',
    'text': '#202124',
    'success': '#0f9d58',
    'error': '#d93025'
}

STYLES = {
    'main_window': {
        'bg': COLORS['background'],
        'size': '1024x768'
    },
    'button': {
        'bg': COLORS['primary'],
        'fg': 'white',
        'font': ('Segoe UI', 12),
        'padding': 15,
        'relief': 'flat',
        'cursor': 'hand2'
    },
    'label': {
        'bg': COLORS['background'],
        'fg': COLORS['text'],
        'font': ('Segoe UI', 11)
    },
    'frame': {
        'bg': COLORS['background'],
        'padding': 20
    }
}
