def ANSI_string(s="", color=None, background=None, bold=False):
        colors = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
            'reset': '\033[0m'
        }
        
        background_colors = {
            'black': '\033[40m',
            'red': '\033[41m',
            'green': '\033[42m',
            'yellow': '\033[43m',
            'blue': '\033[44m',
            'magenta': '\033[45m',
            'cyan': '\033[46m',
            'white': '\033[47m',
            'reset': '\033[0m',
            'gray': '\033[100m',  # 新增的灰色背景
            'light_gray': '\033[47m'  # 新增的淺灰色背景
        }
        
        styles = {
            'bold': '\033[1m',
            'reset': '\033[0m'
        }
        color_code = colors[color] if color in colors else ''
        background_code = background_colors[background] if background in colors else ''
        bold_code = styles['bold'] if bold else ''

        return f"{color_code}{background_code}{bold_code}{s}{styles['reset']}"