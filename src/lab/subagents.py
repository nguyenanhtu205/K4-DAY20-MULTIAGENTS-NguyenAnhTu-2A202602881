"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": "Use when you need to inspect task instructions, documentation, or input files before planning; report facts and edge cases without changing files.",
            "system_prompt": "You are an exploration specialist. Read the requested files, identify requirements and edge cases, and return a concise factual report. Do not modify files.",
        },
        {
            "name": "implementer",
            "description": "Use when a non-trivial implementation or data transformation is needed after the requirements are clear; make the requested changes and verify them.",
            "system_prompt": "You are an implementation specialist. Make only the requested changes, run relevant checks, and report exactly what changed and what you verified.",
        },
        {
            "name": "reviewer",
            "description": "Use when an independent review of a proposed result, tests, or edge cases would reduce the risk of an incorrect final answer; report issues without changing files.",
            "system_prompt": "You are a review specialist. Independently compare the work with the stated requirements, look for edge cases, and return a concise review. Do not modify files.",
        },
    ]
