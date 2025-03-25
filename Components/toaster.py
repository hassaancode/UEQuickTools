import unreal

def show_toast(message, duration=3.0, color=unreal.LinearColor(0, 1, 0, 1)):
    #Displays a toast notification in Unreal Editor.
    unreal.SystemLibrary.print_string(None, message, text_color=color, duration=duration)