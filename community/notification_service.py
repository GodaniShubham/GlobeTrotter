from .models import CommunityNotification


def create_notification(*, recipient, actor=None, kind="system", message="", url="/dashboard/", post=None, reply=None):
    if not recipient or not getattr(recipient, "is_active", True):
        return None
    if actor and getattr(actor, "pk", None) == getattr(recipient, "pk", None):
        return None
    return CommunityNotification.objects.create(
        recipient=recipient,
        actor=actor,
        post=post,
        reply=reply,
        kind=kind,
        message=message[:240],
        url=url[:500],
    )


def notify_trip_created(*, recipient, actor=None, trip_name="your trip", url="/trips/"):
    return create_notification(
        recipient=recipient,
        actor=actor,
        kind="trip_created",
        message=f"Trip created: {trip_name}.",
        url=url,
    )


def notify_trip_updated(*, recipient, actor=None, trip_name="your trip", url="/trips/"):
    return create_notification(
        recipient=recipient,
        actor=actor,
        kind="trip_updated",
        message=f"Trip updated: {trip_name}.",
        url=url,
    )


def notify_trip_shared(*, recipient, actor=None, trip_name="a trip", url="/trips/"):
    return create_notification(
        recipient=recipient,
        actor=actor,
        kind="trip_shared",
        message=f"{actor.get_full_name() if actor else 'Someone'} shared {trip_name} with you.",
        url=url,
    )


def notify_budget_alert(*, recipient, trip_name="your trip", url="/trip/budget/"):
    return create_notification(
        recipient=recipient,
        kind="budget_alert",
        message=f"Budget update for {trip_name}.",
        url=url,
    )
