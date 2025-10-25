# text_compare/views.py
from django.shortcuts import render
from .models import TextComparison
import difflib
import html

def escape_html(s):
    return html.escape(s)

def intraline_html(a, b):
    sm = difflib.SequenceMatcher(None, a, b)
    left_parts = []
    right_parts = []

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            left_parts.append(escape_html(a[i1:i2]))
            right_parts.append(escape_html(b[j1:j2]))
        elif tag == 'replace':
            left_parts.append(f"<span class='chg'>{escape_html(a[i1:i2])}</span>")
            right_parts.append(f"<span class='chg'>{escape_html(b[j1:j2])}</span>")
        elif tag == 'delete':
            left_parts.append(f"<span class='del'>{escape_html(a[i1:i2])}</span>")
        elif tag == 'insert':
            right_parts.append(f"<span class='ins'>{escape_html(b[j1:j2])}</span>")

    return ''.join(left_parts), ''.join(right_parts)

def index(request):
    left_text = ''
    right_text = ''
    diff_rows = []

    if request.method == 'POST':
        left_text = request.POST.get('left_text', '')
        right_text = request.POST.get('right_text', '')

        left_lines = left_text.splitlines()
        right_lines = right_text.splitlines()

        sm = difflib.SequenceMatcher(None, left_lines, right_lines)
        left_num = 1
        right_num = 1

        left_diff_html = ''
        right_diff_html = ''

        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                for li in range(i1, i2):
                    row = {
                        'left_no': left_num,
                        'left_html': escape_html(left_lines[li]),
                        'left_class': '',
                        'right_no': right_num,
                        'right_html': escape_html(right_lines[li - i1 + j1]),
                        'right_class': ''
                    }
                    diff_rows.append(row)
                    left_diff_html += f"<div>{row['left_html']}</div>"
                    right_diff_html += f"<div>{row['right_html']}</div>"
                    left_num += 1
                    right_num += 1
            elif tag == 'replace':
                len_left = i2 - i1
                len_right = j2 - j1
                pairs = max(len_left, len_right)
                for k in range(pairs):
                    a_line = left_lines[i1 + k] if k < len_left else ''
                    b_line = right_lines[j1 + k] if k < len_right else ''
                    left_html, right_html = intraline_html(a_line, b_line)
                    row = {
                        'left_no': left_num if k < len_left else '',
                        'left_html': left_html or '&nbsp;',
                        'left_class': 'removed' if a_line and not b_line else 'changed',
                        'right_no': right_num if k < len_right else '',
                        'right_html': right_html or '&nbsp;',
                        'right_class': 'added' if b_line and not a_line else 'changed'
                    }
                    diff_rows.append(row)
                    left_diff_html += f"<div>{row['left_html']}</div>"
                    right_diff_html += f"<div>{row['right_html']}</div>"
                    if k < len_left: left_num += 1
                    if k < len_right: right_num += 1
            elif tag == 'delete':
                for li in range(i1, i2):
                    row = {
                        'left_no': left_num,
                        'left_html': f"<span class='del'>{escape_html(left_lines[li])}</span>",
                        'left_class': 'removed',
                        'right_no': '',
                        'right_html': '&nbsp;',
                        'right_class': ''
                    }
                    diff_rows.append(row)
                    left_diff_html += f"<div>{row['left_html']}</div>"
                    right_diff_html += "<div>&nbsp;</div>"
                    left_num += 1
            elif tag == 'insert':
                for rj in range(j1, j2):
                    row = {
                        'left_no': '',
                        'left_html': '&nbsp;',
                        'left_class': '',
                        'right_no': right_num,
                        'right_html': f"<span class='ins'>{escape_html(right_lines[rj])}</span>",
                        'right_class': 'added'
                    }
                    diff_rows.append(row)
                    left_diff_html += "<div>&nbsp;</div>"
                    right_diff_html += f"<div>{row['right_html']}</div>"
                    right_num += 1

        # Save input and diffs to DB
        TextComparison.objects.create(
            left_text=left_text,
            right_text=right_text,
            left_diff_html=left_diff_html,
            right_diff_html=right_diff_html
        )

    return render(request, 'text_compare/index.html', {
        'left_text': left_text,
        'right_text': right_text,
        'diff_rows': diff_rows
    })
