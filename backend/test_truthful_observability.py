from main import get_analytics_summary, get_context, get_memories, get_services


def test_mock_services_are_explicitly_synthetic():
    services = get_services(1)
    assert services
    assert all(service.data_mode == "synthetic" for service in services)


def test_context_snapshot_exposes_mode_and_source():
    context = get_context(1)
    assert context["data_mode"] == "synthetic"
    assert context["synthetic"] is True
    assert context["source"] == "repository fixture"
    assert "observed_at" in context


def test_memory_events_expose_mode():
    events = get_memories(1)
    assert events
    assert all(event["data_mode"] == "synthetic" for event in events)


def test_analytics_does_not_claim_measured_savings():
    analytics = get_analytics_summary(1)
    assert analytics["data_mode"] == "synthetic"
    assert analytics["metric_status"] == "unavailable"
    assert analytics["total_saved"] is None
