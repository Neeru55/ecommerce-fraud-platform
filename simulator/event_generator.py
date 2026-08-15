import json
import random
import uuid
from datetime import datetime, timezone, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# Event types that occur in an e-commerce platform
EVENT_TYPES = [
    "product_view",
    "add_to_cart",
    "checkout",
    "payment_success",
    "payment_failed"
]

# Product categories
CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home",
    "Books",
    "Sports"
]


def generate_base_event():
    """
    Generate a realistic e-commerce event.
    This represents a normal event before any network failures or retries.
    """

    event_time = datetime.now(timezone.utc)

    return {
        "event_id": str(uuid.uuid4()),
        "customer_id": random.randint(1000, 99999),
        "session_id": str(uuid.uuid4()),
        "device_id": f"DEV-{random.randint(100, 999)}",
        "event_type": random.choice(EVENT_TYPES),
        "product_id": f"P-{random.randint(1000, 9999)}",
        "category": random.choice(CATEGORIES),
        "price": round(random.uniform(100, 50000), 2),
        "quantity": random.randint(1, 3),
        "city": fake.city(),
        "timestamp": event_time.isoformat()
    }


def inject_duplicate(event):
    """
    Simulate payment gateway retries.

    A duplicate event has the SAME event_id and timestamp,
    representing a retry of the same payment event.
    """

    duplicate = event.copy()
    duplicate["retry_count"] = 1
    return duplicate


def inject_late_event(event):
    """
    Simulate a late-arriving event.

    The event occurred earlier but reached the streaming system later.
    We move the timestamp back by 30-300 seconds.
    """

    late_event = event.copy()

    original_time = datetime.fromisoformat(event["timestamp"])

    delayed_time = original_time - timedelta(
        seconds=random.randint(30, 300)
    )

    late_event["timestamp"] = delayed_time.isoformat()
    late_event["late_event"] = True

    return late_event


def generate_events():
    """
    Generate one or more events.

    Normal event probability: 100%
    Duplicate event probability: 5%
    Late event probability: 10%

    Returns a list because a single event may produce
    additional duplicate/late events.
    """

    events = []

    base_event = generate_base_event()
    events.append(base_event)

    # 5% chance of duplicate event
    if random.random() < 0.05:
        events.append(inject_duplicate(base_event))

    # 10% chance of late event
    if random.random() < 0.10:
        events.append(inject_late_event(base_event))

    return events


def print_events(events):
    """
    Pretty print generated events.
    """

    for index, event in enumerate(events, start=1):
        print(f"\\n===== EVENT {index} =====")
        print(json.dumps(event, indent=2))


if __name__ == "__main__":

    generated_events = generate_events()

    print_events(generated_events)