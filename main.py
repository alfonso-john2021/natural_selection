import random

class Environment:
    def __init__(self, size):
        self.size = size
        self.map = {}
        self.prey = []
        self.predators = []
        self.food = []
        self.generation = 0
        self.max_generations = 100  # Set the maximum number of generations

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

    def check_predator_food(self, predator):
        for food_item in self.food:
            if predator.position == food_item.position:
                self.food.remove(food_item)  # Remove food when predator encounters it
                break  # Exit after consuming one food item

    def next_generation(self):
        if self.generation < self.max_generations:
            self.generation += 1
            self.prey = [self.create_offspring(animal) for animal in self.prey if animal.food_eaten > 0]
            # Optionally, handle predator reproduction or reset if needed

    def create_offspring(self, parent):
        # Create a new animal with mutations inherited from the parent
        child = Animal(
            speed=parent.speed,
            eating_speed=parent.eating_speed,
            color=parent.color
        )
        child.mutate()  # Apply mutation to the child
        return child

class Animal:
    def __init__(self, speed, eating_speed, color):
        self.speed = speed
        self.eating_speed = eating_speed
        self.color = color
        self.position = (random.randint(0, 49), random.randint(0, 49))
        self.food_eaten = 0

    def move(self, env_map):
        # Movement logic here
        pass

    def find_food(self, food):
        # Logic to find and move towards food
        pass

    def eat(self):
        self.food_eaten += 1  # Increase food eaten count

    def check_predators(self, predators):
        for predator in predators:
            if self.is_caught(predator):
                # Check survival
                self.survival_check(predator)

    def is_caught(self, predator):
        return self.position == predator.position

    def survival_check(self, predator):
        # Survival logic based on attributes
        pass

    def mutate(self):
        mutation_type = random.choice(['speed', 'eating_speed', 'color'])
        if mutation_type == 'speed':
            self.speed += random.choice([-1, 1])
        elif mutation_type == 'eating_speed':
            self.eating_speed += random.choice([-1, 1])
        elif mutation_type == 'color':
            self.color = 'black' if self.color == 'white' else 'white'

class Predator:
    def __init__(self):
        self.position = (random.randint(0, 49), random.randint(0, 49))

    def move(self, env_map):
        self.position = (random.randint(0, 49), random.randint(0, 49))

# Initialization and simulation loop
env = Environment(size=50)
for _ in range(10):  # Create initial animals and predators
    env.prey.append(Animal(speed=random.randint(1, 5), eating_speed=random.randint(1, 5), color=random.choice(['white', 'black'])))
    env.predators.append(Predator())
    env.food.append(Food())

# Simulation execution
while env.generation < env.max_generations:
    env.update()
    env.switch_background()
    env.next_generation()  # Handle generation progression
