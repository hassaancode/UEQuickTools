import unreal
import os
import sys

# Add the script directory to Python path
script_dir = os.path.dirname(__file__)
sys.path.append(script_dir)

# Import functions from separate modules

from Components.grouping import group_actors_by_type

menu_owner = "Hassaan Ali"
tool_menus = unreal.ToolMenus.get()
owning_menu_name = "LevelEditor.LevelEditorToolBar.PlayToolBar"


@unreal.uclass()
class Example_SubMenuEntry(unreal.ToolMenuEntryScript):
    def init_as_toolbar_button(self):
        self.data.menu = owning_menu_name
        self.data.advanced.entry_type = unreal.MultiBlockType.TOOL_BAR_COMBO_BUTTON
        self.data.icon = unreal.ScriptSlateIcon("EditorStyle", "Kismet.Tabs.Palette")
        self.data.advanced.style_name_override = "CalloutToolbar"


# Register function globally for menu execution
sys.modules["__main__"].group_actors_by_type = group_actors_by_type

# Avoid multiple registrations
menu_registered = False


def Run():
    global menu_registered

    if menu_registered:
        return

    existing_menu = tool_menus.find_menu(owning_menu_name + ".exampleToolbarEntry")
    if existing_menu:
        tool_menus.remove_menu(owning_menu_name + ".exampleToolbarEntry")

    entry = Example_SubMenuEntry()
    entry.init_as_toolbar_button()
    entry.init_entry(
        menu_owner,
        owning_menu_name,
        "",
        "exampleToolbarEntry",
        "Scripts",
        "Quick Scripts",
    )

    sub_menu = tool_menus.register_menu(
        owning_menu_name + ".exampleToolbarEntry", "", unreal.MultiBoxType.MENU, False
    )

    # Add "Scripts" Section
    sub_menu.add_section("ScriptsSection", "SCRIPTS")

    # Add "Group Actors By Type" Button
    script_entry = unreal.ToolMenuEntryExtensions.init_menu_entry(
        menu_owner,
        "GroupActorsByType",
        "Group Actors By Type",
        "Group all actors in the current level by their type",
        unreal.ToolMenuStringCommandType.PYTHON,
        "",
        "import sys; sys.modules['__main__'].group_actors_by_type()",
    )
    script_entry.set_icon("EditorStyle", "SceneOutliner.NewFolderIcon")
    sub_menu.add_menu_entry("ScriptsSection", script_entry)

    # Add "Support" Section
    sub_menu.add_section("SupportSection", "SUPPORT")

    # Add "Support" Button
    support_entry = unreal.ToolMenuEntryExtensions.init_menu_entry(
        menu_owner,
        "OpenURL",
        "Support",
        "Follow Hassaan Ali on Instagram",
        unreal.ToolMenuStringCommandType.PYTHON,
        "",
        'unreal.SystemLibrary.launch_url("https://www.instagram.com/hassaan_vfx")',
    )
    support_entry.set_icon("EditorStyle", "MessageLog.Url")
    sub_menu.add_menu_entry("SupportSection", support_entry)

    # Extend the toolbar menu
    toolbar = tool_menus.extend_menu(owning_menu_name)
    toolbar.add_menu_entry_object(entry)
    tool_menus.refresh_all_widgets()

    # Mark menu as registered
    menu_registered = True


Run()
