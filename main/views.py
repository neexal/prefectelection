from django.shortcuts import render, redirect
from .models import Voter, Candidate, Position
import json

from django.shortcuts import render, redirect, get_object_or_404
from .models import Voter, Candidate, Position
import json

def landing_page(request):
    voter = None
    message = None
    if request.method == 'POST':
        voting_id = request.POST.get('voting_id')
        if voting_id.isdigit() and len(voting_id) <= 5:
            try:
                voter = Voter.objects.get(voting_id=voting_id)
                if voter.selected_candidates.exists():
                    message = "You have already voted."
                else:
                    request.session['voting_id'] = voting_id
                    return redirect('voting_page')
            except Voter.DoesNotExist:
                message = "Voting ID not found."
        else:
            message = "Invalid voting ID. Please enter up to 5 numeric digits."
    return render(request, 'main/landing_page.html', {'message': message, 'voter': voter})

def voting_page(request):
    if 'voting_id' not in request.session:
        return redirect('landing_page')

    voting_id = request.session['voting_id']
    voter = get_object_or_404(Voter, voting_id=voting_id)

    if voter.selected_candidates.exists():
        del request.session['voting_id']
        return redirect('landing_page')

    if request.method == 'POST':
        selected_candidates_str = request.POST.get('selected_candidates')
        if selected_candidates_str:
            selected_ids = json.loads(selected_candidates_str)
            # Validate selections: 1 school prefect head, 2 school prefect deputy heads
            positions = Position.objects.prefetch_related('candidate_set').all()
            school_head_position = positions.filter(name__iexact='School Prefect Head').first()
            deputy_head_position = positions.filter(name__iexact='School Prefect Deputy Head').first()

            school_head_count = 0
            deputy_head_count = 0

            for cid in selected_ids:
                candidate = Candidate.objects.get(id=cid)
                if candidate.position == school_head_position:
                    school_head_count += 1
                elif candidate.position == deputy_head_position:
                    deputy_head_count += 1

            if school_head_count != 1 or deputy_head_count != 2:
                message = "Please select exactly 1 School Prefect Head and 2 School Prefect Deputy Heads."
                positions = Position.objects.prefetch_related('candidate_set').all()
                return render(request, 'main/voting_page.html', {'positions': positions, 'message': message})

            # Save votes
            voter.selected_candidates.add(*selected_ids)
            for cid in selected_ids:
                candidate = Candidate.objects.get(id=cid)
                candidate.total_votes += 1
                candidate.save()
            del request.session['voting_id']
            return redirect('thank_you')
        else:
            message = "No candidates selected."
            positions = Position.objects.prefetch_related('candidate_set').all()
            return render(request, 'main/voting_page.html', {'positions': positions, 'message': message})

    positions = Position.objects.prefetch_related('candidate_set').all()
    return render(request, 'main/voting_page.html', {'positions': positions, 'voter': voter})


def thank_you(request):
    return render(request, 'main/thank_you_page.html')