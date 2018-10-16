from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    front_page_blocks = []
    news_blocks = []
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True
    data = {
        'user': request.user,
        'front_page_blocks': front_page_blocks,
        'news_blocks': news_blocks,
        'is_logged_in': is_logged_in
    }
    return render(request, 'main/home.html', data)


@login_required(login_url="/accounts/login/")
def profile(request):
    profile = request.user.profile

#     analyses = None
#     reconstructions = None
#     discussed_pieces = []
#
#     if profile.person:
#         analyses = DCAnalysis.objects.filter(analyst=profile.person.person_id).order_by('composition_number')
#         reconstructions = DCReconstruction.objects.filter(reconstructor=profile.person.person_id).order_by('piece')
#
#     comments_by_piece_id = DCComment.objects.filter(author=request.user).order_by('piece')
#     for comment in comments_by_piece_id:
#         if comment.piece not in discussed_pieces:
#             discussed_pieces.append(comment.piece)
#
#     pieces_with_notes = []
#     for piece in DCPiece.objects.all().order_by('piece_id'):
#         if notetext(request.user, piece):
#             pieces_with_notes.append(piece)

    data = {
        'user': request.user,
        'profile': profile,
        #         'favourited_pieces': profile.favourited_piece.order_by('piece_id'),
        #         'favourited_analyses': profile.favourited_analysis.order_by('piece_id'),
        #         'favourited_reconstructions': profile.favourited_reconstruction.order_by('piece'),
        #         'my_analyses': analyses,
        #         'my_reconstructions': reconstructions,
        #         'my_comments': DCComment.objects.filter(author=request.user).order_by('-created'),
        #         'discussed_pieces': discussed_pieces,
        #         'pieces_with_notes': pieces_with_notes,
    }
    return render(
        request,
        'main/profile.html',
        data,
    )


def login(request):
    return render(request, 'main/login.html')
