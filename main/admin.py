from django.contrib import admin
from .models import Position, Candidate, Voter

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'total_votes')
    list_filter = ('position',)
    search_fields = ('name',)

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'display_selected_candidates')
    search_fields = ('voting_id',)

    def display_selected_candidates(self, obj):
        return ", ".join([f"{c.name} ({c.position.name})" for c in obj.selected_candidates.all()])

    display_selected_candidates.short_description = 'Selected Candidates'
