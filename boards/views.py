from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NewTopicForm, PostForm, BuyGiftForm
from .models import Board, Post, Topic, WishList, Gift
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

def shop(request):
    wishlist = get_object_or_404(WishList, name='Bröllop', pk=1)
    return render(request, 'shop.html', {'wishlist': wishlist})

def buy_gift(request, gift_pk):
    wishlist = get_object_or_404(WishList, name='Bröllop', pk=1)
    gift = get_object_or_404(Gift, wishList__name='Bröllop', pk=gift_pk)
    if request.method == 'POST':
        form = BuyGiftForm(request.POST)
        if form.is_valid():
            inp = form.save(commit=False)
            gift.costPayed += inp.costPayed
            gift.latestPayed = inp.costPayed
            if gift.boughtBy_1 == '':
                gift.boughtBy_1 = inp.boughtBy_1
            else:
                if gift.boughtBy_2 == '':
                    gift.boughtBy_2 = inp.boughtBy_1
                else:
                    if gift.boughtBy_3 == '':
                        gift.boughtBy_3 = inp.boughtBy_1
                    else:
                        if gift.boughtBy_4 == '':
                            gift.boughtBy_4 = inp.boughtBy_1
                        else:
                            if gift.boughtBy_4 == '':
                                gift.boughtBy_4 = inp.boughtBy_1
                            else:
                                gift.boughtBy_5 = inp.boughtBy_1
            gift.costLeft = gift.cost - gift.costPayed
            if gift.costLeft == 0:
                gift.bought = True
            gift.save()
            return redirect('thankyou', gift_pk = gift.pk)
    else:
        form = BuyGiftForm()

    return render(request, 'buy_gift.html', {'wishlist': wishlist, 'gift': gift, 'form': form})

def thankyou(request, gift_pk):
    wishlist = get_object_or_404(WishList, name='Bröllop', pk=1)
    gift = get_object_or_404(Gift, wishList__name='Bröllop', pk=gift_pk)
    
    return render(request, 'thankyou.html', {'wishlist': wishlist, 'gift': gift})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now()
            topic.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})