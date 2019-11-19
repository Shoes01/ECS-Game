import cProfile

from game import GameWorld

def main():
    # Prepare world. '1' is the player ID.
    world = GameWorld()
 
    while world.running:
        # Do literally everything.
        world.process()
        
    print('\n\n    Goodbye.\n')

if __name__ == '__main__':
    # cProfile.run('main()', sort='time') # This runs the profiler
    main()