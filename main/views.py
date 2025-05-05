from django.shortcuts import render, redirect
from .models import Voter, Candidate, Position
import json

def landing_page(request):
    if request.method == 'POST':
        voting_id = request.POST.get('voting_id')
        if voting_id.isdigit() and len(voting_id) == 4:
            if Voter.objects.filter(voting_id=voting_id).exists():
                message = "Voting ID is already used."
            else:
                request.session['voting_id'] = voting_id
                return redirect('voting_page')
        else:
            message = "Invalid voting ID. Please enter 4 numeric digits."
    else:
        message = None
    return render(request, 'main/landing_page.html', {'message': message})

def voting_page(request):
    if 'voting_id' not in request.session:
        return redirect('landing_page')

    voting_id = request.session['voting_id']

    if request.method == 'POST':
        selected_candidates_str = request.POST.get('selected_candidates')
        if selected_candidates_str:
            selected_ids = json.loads(selected_candidates_str)
            voter = Voter.objects.create(voting_id=voting_id)
            voter.selected_candidates.add(*selected_ids)
            for cid in selected_ids:
                candidate = Candidate.objects.get(id=cid)
                candidate.total_votes += 1
                candidate.save()
            del request.session['voting_id']
            return redirect('thank_you')
        else:
            del request.session['voting_id']
            return redirect('voting_page')

    positions = Position.objects.prefetch_related('candidate_set').all()
    return render(request, 'main/voting_page.html', {'positions': positions})


def thank_you(request):
    return render(request, 'main/thank_you_page.html')