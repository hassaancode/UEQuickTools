import unreal
from Components.toaster import show_toast  # Import the toast function

def group_actors_by_type():
    """Groups all actors in the level by type and moves them into respective folders."""
    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    all_actors = editor_actor_subsystem.get_all_level_actors()
    actors_by_type = {}

    light_actor_types = [
        "DirectionalLight",
        "SkyAtmosphere",
        "SkyLight",
        "VolumetricFog",
        "ExponentialHeightFog",
        "AtmosphericFog",
    ]

    for actor in all_actors:
        actor_class = actor.get_class().get_name()
        if actor_class in light_actor_types:
            actor_class = "Lights"
        if actor_class not in actors_by_type:
            actors_by_type[actor_class] = []
        actors_by_type[actor_class].append(actor)

    for actor_type, actors in actors_by_type.items():
        folder_path = actor_type
        for actor in actors:
            actor.set_folder_path(folder_path)

    message = f"✅ Grouped {len(all_actors)} actors into {len(actors_by_type)} folders."
    print(message)
    show_toast(message)  # Call the toast function
