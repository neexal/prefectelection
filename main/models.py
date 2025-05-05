from django.db import models

class Position(models.Model):
    name = models.CharField(max_length=100)  # e.g., School Head, Deputy Head

    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='candidates/')
    total_votes = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.name} ({self.position.name})"

class Voter(models.Model):
    voting_id = models.CharField(max_length=100, unique=True)
    selected_candidates = models.ManyToManyField(Candidate)

    def __str__(self):
        return self.voting_id
