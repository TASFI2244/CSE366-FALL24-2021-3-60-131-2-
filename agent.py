class Student:
    def __init__(self, id, availability, preferences):
        self.id = id  # Student ID
        self.availability = availability  # Availability across time slots
        self.preferences = preferences  # Preferences for time slots
        self.schedule = []  # Assigned classes

    def assign_class(self, class_id, time_slot):
        """Assign a class to the student's schedule."""
        if self.availability[time_slot] == 1:  # Ensure availability
            self.schedule.append({"class_id": class_id, "time_slot": time_slot})

    def reset_schedule(self):
        """Clear the student's schedule for a new generation."""
        self.schedule = []
