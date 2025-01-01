import pygame
import numpy as np

class Environment:
    def __init__(self, num_classes, num_students, num_time_slots):
        self.num_classes = num_classes
        self.num_students = num_students
        self.num_time_slots = num_time_slots

        # Define classes with durations and priorities
        self.class_durations = np.random.randint(1, 3, size=num_classes)  # 1-2 hours
        self.class_priorities = np.random.randint(1, 6, size=num_classes)  # Scale of 1-5

        # Students' availability and preferences
        self.student_availability = [
            np.random.choice([0, 1], size=num_time_slots, p=[0.2, 0.8]) for _ in range(num_students)
        ]
        self.student_preferences = [
            np.random.randint(1, 6, size=num_time_slots) for _ in range(num_students)
        ]

    def generate_initial_population(self):
        """
        Generate random schedules as the initial population.
        Each schedule assigns each class to a random student and time slot.
        """
        population = []
        for _ in range(50):
            schedule = [
                {
                    "student": np.random.randint(0, self.num_students),
                    "time_slot": np.random.randint(0, self.num_time_slots),
                }
                for _ in range(self.num_classes)
            ]
            population.append(schedule)
        return population

    def calculate_fitness(self, schedule):
        """
        Calculate the fitness of a schedule. Lower fitness values are better.
        - Conflict penalty: Classes assigned to unavailable students.
        - Preference penalty: Misalignment with student preferences.
        """
        conflict_penalty = 0
        preference_penalty = 0

        for class_id, class_info in enumerate(schedule):
            student = class_info["student"]
            time_slot = class_info["time_slot"]

            # Conflict penalty
            if self.student_availability[student][time_slot] == 0:
                conflict_penalty += 1

            # Preference penalty
            preference_penalty += 1 / self.student_preferences[student][time_slot]

        return conflict_penalty + preference_penalty

    def best_fitness(self, population):
        """
        Find the best (lowest) fitness value in the population.
        """
        return min(self.calculate_fitness(schedule) for schedule in population)

    def max_fitness(self, population):
        """
        Find the worst (highest) fitness value in the population.
        """
        return max(self.calculate_fitness(schedule) for schedule in population)

    def draw_schedule(self, screen, font, schedule):
        """
        Visualize the schedule using Pygame.
        - Rows represent students.
        - Columns represent time slots.
        - Cells show the class priority and highlight conflicts.
        """
        screen.fill((255, 255, 255))  # White background

        # Parameters
        cell_size = 80
        margin_left = 200
        margin_top = 100

        # Display headers for time slots
        for slot in range(self.num_time_slots):
            slot_text = font.render(f"Slot {slot + 1}", True, (0, 0, 0))
            screen.blit(slot_text, (margin_left + slot * cell_size + 10, margin_top - 30))

        # Display the grid
        for student in range(self.num_students):
            # Display student info (availability and preferences)
            availability_text = font.render(
                f"Student {student + 1} (Available: {sum(self.student_availability[student])})",
                True,
                (0, 0, 0),
            )
            screen.blit(availability_text, (10, margin_top + student * cell_size + 20))

            for slot in range(self.num_time_slots):
                rect = pygame.Rect(
                    margin_left + slot * cell_size,
                    margin_top + student * cell_size,
                    cell_size,
                    cell_size,
                )
                pygame.draw.rect(screen, (200, 200, 200), rect)  # Default gray cell
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Border

                # Check for assigned class in the current slot
                assigned_class = None
                for class_id, class_info in enumerate(schedule):
                    if class_info["student"] == student and class_info["time_slot"] == slot:
                        assigned_class = class_id
                        break

                if assigned_class is not None:
                    # Highlight based on priority
                    priority = self.class_priorities[assigned_class]
                    color = (255 - priority * 50, priority * 50, 0)  # Gradient from green to red
                    pygame.draw.rect(screen, color, rect)

                    # Display class info
                    priority_text = font.render(f"P{priority}", True, (255, 255, 255))
                    duration_text = font.render(
                        f"{self.class_durations[assigned_class]}h", True, (255, 255, 255)
                    )
                    screen.blit(priority_text, (rect.x + 10, rect.y + 5))
                    screen.blit(duration_text, (rect.x + 10, rect.y + 30))
