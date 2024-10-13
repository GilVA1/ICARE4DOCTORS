import pygame
import random
import time
from pymongo import MongoClient


pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Reaction Time Test")
WHITE = (255, 255, 255)
RED = (255, 0, 0)


font = pygame.font.SysFont("Arial", 36)


def show_text(message, color, x, y):
    text = font.render(message, True, color)
    screen.blit(text, [x, y])


def reaction_time_test():
    reaction_times = []
    trials = 2  

    for i in range(trials):
        
        screen.fill(WHITE)
        pygame.display.flip()

        
        delay = random.uniform(1, 5)  
        time.sleep(delay)

        
        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, (width//2, height//2), 50)
        pygame.display.flip()

        
        start_time = time.time()

        
        reacting = True
        while reacting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    reaction_time = (time.time() - start_time) * 1000  
                    reaction_times.append(reaction_time)
                    reacting = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

        
        screen.fill(WHITE)
        pygame.display.flip()
        time.sleep(1)  

    
    mean_reaction_time = sum(reaction_times) / len(reaction_times)
    
    return int(mean_reaction_time)



running = True
while running:
    screen.fill(WHITE)
    show_text("Press Space to Start Reaction Test", RED, 100, height//2 - 50)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            mean_time = reaction_time_test()
            screen.fill(WHITE)
            show_text(f"Mean Reaction Time: {mean_time:.0f} ms", RED, 100, height//2 - 50)
            pygame.display.flip()
            time.sleep(5)
            running = False 

        if event.type == pygame.QUIT:
            running = False

pygame.quit()

ans=mean_time

MONGO_URI = 'mongodb+srv://gilvaldezarreola:3p5d3XRxRmlGjoNx@cluster0.uyyqa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)

db = client['HOSPITAL']  
collection = db['DOCTOR']

new_document = {
    
    "reactionTime":ans,
    "teamId":8,
    "redness":88,
    "heartBeats":40,
    "pupils":22
}

result = collection.insert_one(new_document)

print(f"Document inserted with _id: {result.inserted_id}")