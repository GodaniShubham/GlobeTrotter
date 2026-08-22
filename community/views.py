import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Exists, F, OuterRef, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator

from .forms import CommunityPostForm, CommunityReplyForm, CommunityReportForm
from .models import (
    CommunityLike,
    CommunityNotification,
    CommunityPost,
    CommunityReply,
    CommunityReplyLike,
    CommunityReport,
    CommunitySave,
    CommunityShare,
)

CATEGORY_CHOICES = dict(CommunityPost.CATEGORY_CHOICES)


def _annotated_posts(request, queryset):
    base = queryset.annotate(
        reply_count=Count("replies", filter=Q(replies__is_published=True), distinct=True),
        like_count=Count("likes", distinct=True),
        save_count=Count("saves", distinct=True),
    )
    if request.user.is_authenticated:
        base = base.annotate(
            is_liked=Exists(
                CommunityLike.objects.filter(post=OuterRef("pk"), user=request.user)
            ),
            is_saved=Exists(
                CommunitySave.objects.filter(post=OuterRef("pk"), user=request.user)
            ),
        )
    return base


def _annotated_replies(request, queryset):
    base = queryset.annotate(like_count=Count("likes", distinct=True))
    if request.user.is_authenticated:
        base = base.annotate(
            is_liked=Exists(
                CommunityReplyLike.objects.filter(reply=OuterRef("pk"), user=request.user)
            )
        )
    return base


def _display_name(user):
    return user.get_full_name().strip() or user.username


def _initials(user):
    first = (user.first_name or "")[:1]
    last = (user.last_name or "")[:1]
    return (first + last or user.username[:2]).upper()


def _notify(*, recipient, actor, kind, message, url, post=None, reply=None):
    if not recipient or not recipient.is_active or recipient.pk == getattr(actor, "pk", None):
        return
    # Avoid unread notification spam from the same interaction while preserving
    # subsequent interactions after the notification has been read.
    existing = CommunityNotification.objects.filter(
        recipient=recipient,
        actor=actor,
        kind=kind,
        post=post,
        reply=reply,
        is_read=False,
    ).first()
    if not existing:
        CommunityNotification.objects.create(
            recipient=recipient,
            actor=actor,
            post=post,
            reply=reply,
            kind=kind,
            message=message,
            url=url,
        )


def _notify_mentions(*, actor, body, post, reply=None):
    for username in set(re.findall(r"@([A-Za-z0-9_.-]{2,50})", body or "")):
        recipient = None
        from django.contrib.auth import get_user_model
        User = get_user_model()
        recipient = User.objects.filter(username__iexact=username, is_active=True).first()
        if recipient:
            _notify(
                recipient=recipient,
                actor=actor,
                kind="mention",
                message=f"{_display_name(actor)} mentioned you in a community conversation.",
                url=reverse("community_post", args=[post.pk]),
                post=post,
                reply=reply,
            )


@require_GET
def feed(request):
    category = request.GET.get("category", "").strip().lower()
    query = " ".join(request.GET.get("q", "").split())
    sort = request.GET.get("sort", "hot").strip().lower()
    if sort not in {"hot", "new", "top"}:
        sort = "hot"

    posts = (
        CommunityPost.objects.filter(is_published=True)
        .select_related("author", "city")
    )

    if category not in CATEGORY_CHOICES:
        category = ""
    elif category:
        posts = posts.filter(category=category)

    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(body__icontains=query)
            | Q(city__name__icontains=query)
            | Q(city__country__icontains=query)
            | Q(author__first_name__icontains=query)
            | Q(author__last_name__icontains=query)
            | Q(author__username__icontains=query)
        )

    posts = _annotated_posts(request, posts)
    if sort == "new":
        posts = posts.order_by("-created_at")
    elif sort == "top":
        posts = posts.order_by("-like_count", "-reply_count", "-save_count", "-created_at")
    else:
        posts = posts.annotate(
            hot_score=F("like_count") * 2 + F("reply_count") * 4 + F("save_count") * 2
        ).order_by("-hot_score", "-created_at")

    paginator = Paginator(posts, 15)
    page_obj = paginator.get_page(request.GET.get("page"))

    popular_posts = (
        _annotated_posts(
            request,
            CommunityPost.objects.filter(is_published=True).order_by(),
        )
        .order_by("-like_count", "-reply_count", "-save_count", "-created_at")[:6]
    )

    context = {
        "posts": page_obj.object_list,
        "page_obj": page_obj,
        "popular_posts": popular_posts,
        "selected_category": category,
        "search_query": query,
        "sort": sort,
        "total_results": paginator.count,
        "categories": CommunityPost.CATEGORY_CHOICES,
        "active": "community",
        "page_title": "Community — GlobeTrotter",
    }
    return render(request, "pages/community.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = CommunityPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_ip = request.META.get("REMOTE_ADDR")
            post.save()
            _notify_mentions(actor=request.user, body=post.body, post=post)
            messages.success(request, "Your post is live in the community.")
            return redirect("community_post", pk=post.pk)
    else:
        form = CommunityPostForm()
    return render(
        request,
        "pages/community_new_post.html",
        {"form": form, "active": "community", "page_title": "New post — GlobeTrotter"},
    )


def _reply_rows(request, post):
    replies = list(
        _annotated_replies(
            request,
            CommunityReply.objects.filter(post=post, is_published=True)
            .select_related("author", "parent")
            .order_by("created_at"),
        )
    )
    grouped = {}
    for reply in replies:
        grouped.setdefault(reply.parent_id, []).append(reply)

    rows = []

    def walk(parent_id=None, depth=0):
        for reply in grouped.get(parent_id, []):
            reply.depth = min(depth, 4)
            reply.author_display = _display_name(reply.author)
            reply.initials = _initials(reply.author)
            rows.append(reply)
            walk(reply.pk, depth + 1)

    walk()
    return rows


@require_GET
def post_detail(request, pk):
    post = get_object_or_404(
        CommunityPost.objects.select_related("author", "city"),
        pk=pk,
        is_published=True,
    )
    post = _annotated_posts(request, CommunityPost.objects.filter(pk=pk)).first()
    replies = _reply_rows(request, post)
    reply_form = (
        CommunityReplyForm()
        if request.user.is_authenticated and post.comments_enabled
        else None
    )
    report_form = (
        CommunityReportForm()
        if request.user.is_authenticated and request.user != post.author
        else None
    )
    popular_posts = _annotated_posts(
        request,
        CommunityPost.objects.filter(is_published=True).exclude(pk=pk).order_by(),
    ).order_by("-like_count", "-reply_count", "-save_count", "-created_at")[:5]

    return render(
        request,
        "pages/community_post.html",
        {
            "post": post,
            "replies": replies,
            "reply_form": reply_form,
            "report_form": report_form,
            "popular_posts": popular_posts,
            "active": "community",
            "page_title": f"{post.title} — Community",
        },
    )


@login_required
@require_POST
def reply_to_post(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk, is_published=True)
    if not post.comments_enabled:
        return JsonResponse({"ok": False, "message": "Replies are closed for this post."}, status=400)

    parent_id = request.POST.get("parent_id") or None
    parent = None
    if parent_id:
        parent = get_object_or_404(
            CommunityReply,
            pk=parent_id,
            post=post,
            is_published=True,
        )

    form = CommunityReplyForm(request.POST)
    if not form.is_valid():
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)
        messages.error(request, "Please check your reply and try again.")
        return redirect("community_post", pk=pk)

    with transaction.atomic():
        reply = form.save(commit=False)
        reply.post = post
        reply.parent = parent
        reply.author = request.user
        reply.created_ip = request.META.get("REMOTE_ADDR")
        reply.save()

        if parent and parent.author_id != request.user.id:
            _notify(
                recipient=parent.author,
                actor=request.user,
                kind="reply_reply",
                message=f"{_display_name(request.user)} replied to your comment.",
                url=reverse("community_post", args=[post.pk]),
                post=post,
                reply=reply,
            )
        elif post.author_id != request.user.id:
            _notify(
                recipient=post.author,
                actor=request.user,
                kind="post_reply",
                message=f"{_display_name(request.user)} replied to your post.",
                url=reverse("community_post", args=[post.pk]),
                post=post,
                reply=reply,
            )
        _notify_mentions(actor=request.user, body=reply.body, post=post, reply=reply)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "ok": True,
                "reply": {
                    "id": reply.pk,
                    "parent_id": reply.parent_id,
                    "author": _display_name(request.user),
                    "initials": _initials(request.user),
                    "body": reply.body,
                    "created_at": reply.created_at.isoformat(),
                    "like_count": 0,
                    "is_liked": False,
                },
                "reply_count": CommunityReply.objects.filter(
                    post=post, is_published=True
                ).count(),
            }
        )

    messages.success(request, "Reply added.")
    return redirect("community_post", pk=pk)


@login_required
@require_POST
def toggle_like(request, pk):
    with transaction.atomic():
        post = get_object_or_404(
            CommunityPost.objects.select_for_update(),
            pk=pk,
            is_published=True,
        )
        like, created = CommunityLike.objects.get_or_create(
            post=post,
            user=request.user,
            defaults={"created_ip": request.META.get("REMOTE_ADDR")},
        )
        if not created:
            like.delete()
        elif post.author_id != request.user.id:
            _notify(
                recipient=post.author,
                actor=request.user,
                kind="post_like",
                message=f"{_display_name(request.user)} liked your post.",
                url=reverse("community_post", args=[post.pk]),
                post=post,
            )

    return JsonResponse(
        {
            "ok": True,
            "liked": created,
            "count": CommunityLike.objects.filter(post=post).count(),
        }
    )


@login_required
@require_POST
def toggle_save(request, pk):
    with transaction.atomic():
        post = get_object_or_404(
            CommunityPost.objects.select_for_update(),
            pk=pk,
            is_published=True,
        )
        saved, created = CommunitySave.objects.get_or_create(
            post=post,
            user=request.user,
            defaults={"created_ip": request.META.get("REMOTE_ADDR")},
        )
        if not created:
            saved.delete()

    return JsonResponse(
        {
            "ok": True,
            "saved": created,
            "count": CommunitySave.objects.filter(post=post).count(),
        }
    )


@login_required
@require_POST
def toggle_reply_like(request, pk):
    with transaction.atomic():
        reply = get_object_or_404(
            CommunityReply.objects.select_for_update().select_related("author", "post"),
            pk=pk,
            is_published=True,
        )
        like, created = CommunityReplyLike.objects.get_or_create(
            reply=reply,
            user=request.user,
            defaults={"created_ip": request.META.get("REMOTE_ADDR")},
        )
        if not created:
            like.delete()
        elif reply.author_id != request.user.id:
            _notify(
                recipient=reply.author,
                actor=request.user,
                kind="reply_like",
                message=f"{_display_name(request.user)} liked your comment.",
                url=reverse("community_post", args=[reply.post_id]),
                post=reply.post,
                reply=reply,
            )

    return JsonResponse(
        {
            "ok": True,
            "liked": created,
            "count": CommunityReplyLike.objects.filter(reply=reply).count(),
        }
    )


@login_required
@require_POST
def delete_reply(request, pk):
    reply = get_object_or_404(
        CommunityReply.objects.select_related("post"),
        pk=pk,
        is_published=True,
    )
    if reply.author_id != request.user.id and not request.user.is_staff:
        return JsonResponse({"ok": False, "message": "Not allowed."}, status=403)

    reply.is_published = False
    reply.save(update_fields=["is_published", "updated_at"])
    return JsonResponse({"ok": True, "reply_id": reply.pk})


@login_required
@require_GET
def saved_posts(request):
    posts = (
        CommunityPost.objects.filter(is_published=True, saves__user=request.user)
        .select_related("author", "city")
        .distinct()
    )
    posts = _annotated_posts(request, posts)
    return render(
        request,
        "pages/community_saved.html",
        {
            "posts": posts,
            "active": "community",
            "page_title": "Saved conversations — GlobeTrotter",
        },
    )


@login_required
@require_POST
def report_post(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk, is_published=True)
    if request.user == post.author:
        messages.error(request, "You cannot report your own post.")
        return redirect("community_post", pk=pk)
    form = CommunityReportForm(request.POST)
    if form.is_valid():
        report, created = CommunityReport.objects.get_or_create(
            post=post,
            reporter=request.user,
            defaults={
                "reason": form.cleaned_data["reason"],
                "note": form.cleaned_data["note"],
            },
        )
        if created:
            messages.success(request, "Thanks. Your report has been recorded.")
        else:
            messages.info(request, "You have already reported this post.")
    else:
        messages.error(request, "Please select a report reason.")
    return redirect("community_post", pk=pk)


@login_required
@require_POST
def delete_post(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    if post.author_id != request.user.id and not request.user.is_staff:
        return JsonResponse({"ok": False, "message": "Not allowed."}, status=403)
    post.is_published = False
    post.save(update_fields=["is_published", "updated_at"])
    return JsonResponse({"ok": True, "post_id": post.pk})



@login_required
@require_POST
def record_share(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk, is_published=True)
    channel = (request.POST.get("channel") or "copy").lower()
    valid = {value for value, _label in CommunityShare.CHANNEL_CHOICES}
    if channel not in valid:
        return JsonResponse({"ok": False, "message": "Unsupported share channel."}, status=400)

    CommunityShare.objects.create(
        post=post,
        user=request.user,
        channel=channel,
        created_ip=request.META.get("REMOTE_ADDR"),
    )
    return JsonResponse({
        "ok": True,
        "share_count": CommunityShare.objects.filter(post=post).count(),
    })


@login_required
@require_GET
def notifications(request):
    rows = list(
        CommunityNotification.objects
        .filter(recipient=request.user)
        .select_related("actor", "post")
        .order_by("-created_at")[:25]
    )
    unread = CommunityNotification.objects.filter(
        recipient=request.user, is_read=False
    ).count()

    payload = []
    for item in rows:
        payload.append({
            "id": item.pk,
            "message": item.message,
            "url": item.url,
            "kind": item.kind,
            "read": item.is_read,
            "created_at": item.created_at.isoformat(),
            "actor": _display_name(item.actor) if item.actor else "",
        })

    return JsonResponse({"ok": True, "unread": unread, "items": payload})


@login_required
@require_POST
def mark_notifications_read(request):
    notification_id = request.POST.get("id")
    qs = CommunityNotification.objects.filter(
        recipient=request.user, is_read=False
    )
    if notification_id and notification_id.isdigit():
        qs = qs.filter(pk=int(notification_id))
    qs.update(is_read=True)
    return JsonResponse({"ok": True})


@login_required
@require_GET
def post_updates(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk, is_published=True)
    replies = _reply_rows(request, post)

    return JsonResponse({
        "ok": True,
        "post_id": post.pk,
        "reply_count": len(replies),
        "like_count": CommunityLike.objects.filter(post=post).count(),
        "save_count": CommunitySave.objects.filter(post=post).count(),
        "replies": [
            {
                "id": r.pk,
                "parent_id": r.parent_id,
                "depth": r.depth,
                "author": r.author_display,
                "initials": r.initials,
                "body": r.body,
                "created_at": r.created_at.isoformat(),
                "like_count": r.like_count,
                "is_liked": getattr(r, "is_liked", False),
                "is_author": r.author_id == request.user.id,
            }
            for r in replies
        ],
    })
