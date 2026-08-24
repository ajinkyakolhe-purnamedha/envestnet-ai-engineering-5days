"""The advisor workflow has two production owners."""


def test_analysis_report_and_client_list_owner_exports_its_behavior():
    from chronos.advisor_analysis_reports_and_client_lists import (
        analyze_client_portfolio,
        build_advisor_recommendations,
        generate_advisor_review_report,
        list_clients_for_advisor,
    )
    assert all(function.__module__ == "chronos.advisor_analysis_reports_and_client_lists" for function in (
        analyze_client_portfolio,
        build_advisor_recommendations,
        generate_advisor_review_report,
        list_clients_for_advisor,
    ))


def test_m9_draft_and_approval_legacy_paths_delegate_to_owner():
    from chronos.advisor_assistant_drafts_and_approval import (
        answer_with_memory,
        decide_note_draft,
        list_approved_notes_for_client,
        list_pending_drafts_for_advisor,
        submit_note_for_approval,
    )
    from labs.m9_advisor_assistant.answer_with_memory import (
        answer_with_memory as legacy_answer_with_memory,
    )
    from labs.m9_advisor_assistant.decide_note_draft import (
        decide_note_draft as legacy_decide,
    )
    from labs.m9_advisor_assistant.note_draft_queries import (
        list_approved_notes_for_client as legacy_approved,
        list_pending_drafts_for_advisor as legacy_pending,
    )
    from labs.m9_advisor_assistant.submit_note_for_approval import (
        submit_note_for_approval as legacy_submit,
    )

    # The M9 memory wrapper keeps its deliberately patchable lab seam;
    # the production route imports the owner directly.
    assert legacy_answer_with_memory is not answer_with_memory
    assert legacy_decide is decide_note_draft
    assert legacy_approved is list_approved_notes_for_client
    assert legacy_pending is list_pending_drafts_for_advisor
    assert legacy_submit is submit_note_for_approval
