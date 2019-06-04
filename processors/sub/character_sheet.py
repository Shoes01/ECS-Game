def render_character_sheet(world):
    if not world.state == 'ViewCharacterSheet':
        return 0
    
    # Use the Map console
    # Display base stats, soul, and total stats
    # Displays item slots and their items
    # Print to Map