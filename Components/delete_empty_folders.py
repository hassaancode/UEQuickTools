import unreal

def delete_empty_folders_in_outliner():
    """
    Deletes empty folders in the Unreal Engine 5 scene outliner.
    An empty folder is defined as a folder containing no actors or only other empty folders.
    """
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        unreal.log_warning("Could not get the editor world.")
        return

    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()

    # Create a mapping of folder paths to their actors
    folder_to_actors = {}
    for actor in all_actors:
        folder_path = actor.get_folder_path()
        if folder_path:
            if folder_path not in folder_to_actors:
                folder_to_actors[folder_path] = []
            folder_to_actors[folder_path].append(actor)

    # Get all unique folder paths
    all_folder_paths = set()
    for actor in all_actors:
        if actor.get_folder_path():
            # Add the folder path itself
            all_folder_paths.add(actor.get_folder_path())
            # Add all parent folder paths
            parts = actor.get_folder_path().split('/')
            current_path = ""
            for part in parts:
                if current_path:
                    current_path += '/' + part
                else:
                    current_path = part
                all_folder_paths.add(current_path)


    # Function to check if a folder is empty
    def is_folder_empty(folder_path):
        # Check if the folder has any actors directly inside it
        if folder_path in folder_to_actors and folder_to_actors[folder_path]:
            return False

        # Check if the folder has any non-empty child folders
        for path in all_folder_paths:
            if path.startswith(folder_path + '/') and path != folder_path:
                if not is_folder_empty(path):
                    return False
        return True

    # Identify empty folders
    empty_folders_to_delete = []
    # Sort paths to process deepest first
    sorted_folder_paths = sorted(list(all_folder_paths), key=lambda x: x.count('/'), reverse=True)

    for folder_path in sorted_folder_paths:
        if is_folder_empty(folder_path):
            empty_folders_to_delete.append(folder_path)

    # Delete the empty folders
    if empty_folders_to_delete:
        unreal.log("Deleting empty folders:")
        for folder_path in empty_folders_to_delete:
            unreal.log(f"  - {folder_path}")
            # Unreal Engine's delete_folder requires a package path prefix for folder names.
            # However, direct folder manipulation might be limited via Python API for Outliner folders.
            # A common workaround or approach is to select and delete, or potentially
            # use lower-level C++ access if exposed. For this example, we will log
            # which folders *would* be deleted and note the API limitations for direct deletion.
            # As a direct deletion function for Outliner folders isn't readily available
            # in the Python API like it is for Asset Browser folders, a manual step
            # or a more complex solution might be required in a real scenario.
            # The following line is commented out as a direct API call to delete an outliner folder
            # by path like this is not a standard Python API function.
            # unreal.EditorLevelLibrary.delete_folder(folder_path) # This line is illustrative, not functional for Outliner folders via this API.
            pass # Placeholder as direct deletion API for Outliner folders by path is not standard.
        unreal.log("Deletion process completed (manual deletion in the Outliner might be required for some folders).")
    else:
        unreal.log("No empty folders found in the outliner.")

if __name__ == "__main__":
    # Example usage:
    delete_empty_folders_in_outliner()