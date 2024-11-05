import random
import time  # To manage the tick timing
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pandas as pd
class Environment:
    def __init__(self, size):
        self.size = size
        self.map = {}
        self.prey = []
        self.predators = []
        self.food = []
        self.generation = 0
        self.background_color = 'white'  # Default background color is white
        self.max_generations = 10  # Maximum number of generations
        self.ticks_per_generation = 500  # Number of ticks per generation
        self.current_ticks = 0  # Track current ticks in the generation
        self.avg_speed = 1 # Sample average speed for first survival check
        self.data = []
    def switch_background(self):
        self.background_color = 'black' if self.background_color == 'white' else 'white'

    def update(self):
        for predator in self.predators:
            predator.move(self.map)
            self.check_predator_food(predator)

        for animal in self.prey:
            animal.move(self.map)
            if animal.find_food(self.food):
                animal.eat()

            animal.check_predators(self.predators)
        for _ in range(5): # Re-fill the food
            env.food.append(Food())

    def check_predator_food(self, predator):
        for food_item in self.food:
            if predator.position == food_item.position:
                self.food.remove(food_item)  # Remove food when predator encounters it
                break  # Exit after consuming one food item

    def next_generation(self):
        if self.generation < self.max_generations:
            self.generation += 1
            surviving_prey = [animal for animal in self.prey if animal.food_eaten >= (self.generation)/4]
            #surviving_prey = [animal for animal in self.prey if animal.food_eaten >= 1] # less harsh
            self.prey = [self.create_offspring(animal) for animal in surviving_prey]
            #self.prey.extend([self.create_offspring(animal) for animal in surviving_prey]) #double the child
            total_predators = [predator for predator in self.predators]
            total_predators_killed_white = sum(a.killed_white for a in total_predators)
            total_predators_killed_black = sum(a.killed_black for a in total_predators)
            # Print important values
            try:
                animal = random.choice(surviving_prey)  # Choose a random animal
            except:
                print("All animal instances were died, end the simulation")
                quit()
            avg_speed = sum(a.speed for a in surviving_prey) / len(surviving_prey)
            avg_food_eaten = sum(a.food_eaten for a in surviving_prey) / len(surviving_prey)
            colors = [a.color for a in surviving_prey]
            color_black = colors.count("black")
            color_white = colors.count("white")
            
            print(f"Generation {self.generation}:")
            print(f"Survived Animals: {len(surviving_prey)}:")
            #print(f"Total Predators: {len(total_predators)}:")
            print(f"Total Predators_kill_white: {total_predators_killed_white}")
            print(f"Total Predators_kill_black: {total_predators_killed_black}")
            #print(f"Total Animals died by hunger: {len([animal for animal in self.prey if animal.food_eaten < 1])}:") need patch
            print(f"Random Animal - Food Count: {animal.food_eaten}, Speed: {animal.speed}, Color: {animal.color}")
            print(f"Average Speed of Surviving Animals: {avg_speed:.2f}")
            print(f"Average Food Eaten by Surviving Animals: {avg_food_eaten:.2f}")
            print(f"Colors of Surviving Animals: {', '.join(set(colors))}")
            print(f"Black: {color_black}")
            print(f"White: {color_white}")
            print("-" * 30)  # Separator for clarity
            # for statistics
            #'Total Predators_kill': total_predators_killed,
            self.data.append({
                'Generation': self.generation,
                'Surviving Animals': len(surviving_prey),
                'Total of White Killed By Predator': total_predators_killed_white,
                'Total of Black Killed By Predator': total_predators_killed_black,
                'Average Speed of Surviving Animals': round(avg_speed,1),
                'Average Food Eaten by Surviving Animals': round(avg_food_eaten,1),
                'Colors of Surviving Animals': ', '.join(set(colors)),
                'Black': color_black,
                'White': color_white
            })


    def create_offspring(self, parent):
        child = Animal(
            speed=parent.speed,
            eating_speed=parent.eating_speed,
            color=parent.color
        )
        child.mutate()  # Apply mutation to the child
        return child

    def render_map(self):
        # Create a 30x30 grid initialized with empty spaces
        grid = [['.' for _ in range(self.size)] for _ in range(self.size)]

        # Place food on the grid
        for food_item in self.food:
            grid[food_item.position[0]][food_item.position[1]] = 'F'  # F for food

        # Place predators on the grid
        for predator in self.predators:
            grid[predator.position[0]][predator.position[1]] = 'P'  # P for predator

        # Place prey on the grid
        for animal in self.prey:
            grid[animal.position[0]][animal.position[1]] = 'A'  # A for animal

        # Print the grid
        print("Generation:", self.generation)
        for row in grid:
            print(' '.join(row))
        print()  # Newline for better readability

class Animal:
    def __init__(self, speed, eating_speed, color):
        self.speed = speed  # Speed determines how far the animal can move
        self.eating_speed = eating_speed
        self.color = color
        self.position = (random.randint(0, 29), random.randint(0, 29))
        self.food_eaten = 0

    def move(self, env_map):
        # Move one step in a random direction based on speed
        direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])  # Random direction
        new_position = (self.position[0] + direction[0] * self.speed,
                        self.position[1] + direction[1] * self.speed)

        # Ensure the new position is within bounds
        self.position = (max(0, min(new_position[0], self.map_size() - 1)),
                         max(0, min(new_position[1], self.map_size() - 1)))

    def map_size(self):
        return 30  # Assuming the environment is 30x30

    def find_food(self, food):
        return any(self.position == food_item.position for food_item in food)

    def eat(self):
        self.food_eaten += 1  # Increase food eaten count
        self.food_eaten += self.speed * 0.25 # Faster speed advantage (원래는 이동할때 계산해야하나 실력한계로 가중치로 해결)
        for food_item in env.food:
            if self.position == food_item.position:
                env.food.remove(food_item)
    def check_predators(self, predators):
        for predator in predators:
            if self.is_caught(predator):
                #print("Debug: I caught!!!")
                self.survival_check(predator)

    def is_caught(self, predator):
        return self.position == predator.position

    def survival_check(self, predator):
        # Survival logic based on attributes
        # survival values = speed, opposite color, eating Speed
        # disadvantage values = same color, low speed
        survival_check = 100
        
        if self.speed <= env.avg_speed :
            survival_check -= 10
        if self.color != env.background_color :
            survival_check -= 80
        survival_advantage = self.speed * self.eating_speed
        survival_check +=survival_advantage
        if random.randint(0,100) <= survival_check :
            pass # survived
        else : # remove in next generation
            self.speed = 0
            if self.color == "white":
                predator.killed_white+=1
            else:
                predator.killed_black+=1
            env.prey.remove(self)
            #print("plue 1")
    def mutate(self):
        mutation_type = random.choice(['speed', 'eating_speed', 'color'])
        if mutation_type == 'speed':
            self.speed += random.choice([-3,-2,-1, 1, 2, 3])
            if self.speed <= 0 :
                self.speed = 0
        elif mutation_type == 'eating_speed':
            self.eating_speed += random.choice([-3,-2,-1, 1, 2, 3])
            if self.eating_speed <= 0 :
                self.eating_speed = 0
        elif mutation_type == 'color':
            if self.color == 'white':
                if random.random() >= 0.25:
                    pass
                else :
                    self.color = 'black'
            if self.color == 'black':
                if random.random() >= 0.25:
                    pass
                else :
                    self.color = 'white'

class Predator:
    def __init__(self):
        self.position = (random.randint(0, 29), random.randint(0, 29))
        self.killed_white = 0
        self.killed_black = 0
    def move(self, env_map):
        self.position = (random.randint(0, 29), random.randint(0, 29))
class Food:
    def __init__(self):
        self.position = (random.randint(0, 29), random.randint(0, 29))


# Initialization and simulation loop
env = Environment(30)
for _ in range(300):  # Create initial animals and predators
    env.prey.append(Animal(speed=random.randint(1, 5), eating_speed=random.randint(1, 5), color=random.choice(['white', 'black'])))
    for _ in range(1):
        env.food.append(Food())
env.predators.append(Predator())
# Simulation execution
ticks_per_second = 50000  # Number of ticks per second
tick_duration = 1.0 / ticks_per_second  # Duration of each tick in seconds
#debug
print("Generation 0:")
colors = [a.color for a in env.prey]
color_black = colors.count("black")
color_white = colors.count("white")
print(f"Black: {color_black}")
print(f"White: {color_white}")
while env.generation < env.max_generations:
    start_time = time.time()
    
    env.update()  # Update the state of the environment
    #env.render_map()
    env.current_ticks += 1  # Increment the tick counter

    # Check if we've reached the number of ticks for the current generation
    if env.current_ticks >= env.ticks_per_generation:
        env.current_ticks = 0  # Reset the tick counter
        
        #env.predators.append(Predator()) # each generation, 1 predator is added
        env.next_generation() # Handle generation progression
        env.switch_background() 
    elapsed_time = time.time() - start_time
    time_to_sleep = tick_duration - elapsed_time
    if time_to_sleep > 0:
        time.sleep(time_to_sleep)  # Sleep to maintain the tick rate

#print(env.data)
df = pd.DataFrame(env.data)
name = "simulation_data" + str(time.time()) + ".xlsx"
df.to_excel(name, index=False)

