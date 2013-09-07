from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import Http404
from moodboard.models import Board, Image, Comment
from moodboard.forms import ImageForm, BoardForm, CommentForm

from django.http import HttpResponse

def index(request):
	boards = Board.objects.all()
	return render(request, 'index.html', {'boards':boards})

def board(request, slug):
	try:
		board = Board.objects.get(slug=slug)
		images = Image.objects.filter(board=board.pk)

		if images.count() > 0:
			return render(request, 'board.html', {'board':board, 'images':images})
		else:
			return render(request, 'board.html', {'board':board,'message':'No images have been added to this board!'})
	except Board.DoesNotExist:
		raise Http404

def createImage(request, slug):
	board = Board.objects.get(slug=slug)

	if request.method == 'POST':
		form = ImageForm(request.POST)

		if form.is_valid():
			form.save()
			return render(request, 'createImage.html', {'message':'Added new image', 'board':board})
		else:
			return render(request, 'createImage.html', {'message':'Whoops! There seems to be an error!', 'errors':form.errors, 'board':board})
	else:
		return render(request, 'createImage.html', {'board':board})

def createBoard(request):
	if request.method == 'POST':
		form = BoardForm(request.POST)

		if form.is_valid():
			form.save()
			return render(request, 'createBoard.html', {'message':'Board "{0}" created!'.format(form.cleaned_data['name'])})
		else:
			return render(request, 'createBoard.html', {'message':'Whoops! There seems to be an error!', 'errors':form.errors})
	else:
		return render(request, 'createBoard.html')

def comments(request, slug, iid):
	comments = Comment.objects.filter(image=iid)
	board = Board.objects.get(slug=slug)
	image = Image.objects.get(pk=iid)

	if request.method == 'POST':
		form = CommentForm(request.POST)

		if form.is_valid():
			form.save()
			return render(request, 'comments.html', {'message':'Comment added', 'comments':comments, 'image':image, 'board':board})
		else:
			return render(request, 'comments.html', {'message':'Whoops! There seems to be an error!', 'errors':form.errors, 'comments':comments, 'image':image, 'board':board})

	else:

		if comments.count() > 0:
			return render(request, 'comments.html', {'comments':comments, 'image':image, 'board':board})
		else:
			return render(request, 'comments.html', {'message':'No comments have been left on this image yet :(', 'comments':comments, 'image':image, 'board':board})
