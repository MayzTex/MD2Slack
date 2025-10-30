import pytest
from md2slack import SlackMarkdown

def test_headers():
    parser = SlackMarkdown()
    assert parser("# Heading 1") == "*Heading 1*"
    assert parser("## Heading 2") == "*Heading 2*"
    assert parser("### Heading 3") == "*Heading 3*"
    assert parser("#### Heading 4") == "*Heading 4*"
    assert parser("##### Heading 5") == "*Heading 5*"
    assert parser("###### Heading 6") == "*Heading 6*"

def test_bold_italic():
    parser = SlackMarkdown()
    assert parser("**Bold**") == "*Bold*"
    assert parser("*Italic*") == "_Italic_"
    assert parser("***Bold Italic***") == "*_Bold Italic_*"
    assert parser("__Bold__") == "*Bold*"
    assert parser("_Italic_") == "_Italic_"
    assert parser("___Bold Italic___") == "*_Bold Italic_*"

def test_strikethrough():
    parser = SlackMarkdown()
    assert parser("~Strikethrough~") == "~Strikethrough~"

def test_inline_code():
    parser = SlackMarkdown()
    assert parser("`Inline Code`") == "`Inline Code`"

def test_code_block():
    parser = SlackMarkdown()
    markdown = """```
def hello():
    print("Hello, Slack!")
```"""
    expected_output = """```
def hello():
    print("Hello, Slack!")
```"""
    assert parser(markdown) == expected_output

def test_lists():
    parser = SlackMarkdown()
    assert parser("- Item 1\n- Item 2") == "• Item 1\n• Item 2"
    assert parser("1. First\n2. Second") == "1. First\n2. Second"
    assert parser("* Item A\n* Item B") == "• Item A\n• Item B"

def test_nested_lists():
    parser = SlackMarkdown()
    markdown = "- Item 1\n  - Subitem 1.1\n  - Subitem 1.2\n- Item 2"
    expected_output = "• Item 1\n  • Subitem 1.1\n  • Subitem 1.2\n• Item 2"
    assert parser(markdown) == expected_output

def test_numbered_list_resets_after_paragraph():
    parser = SlackMarkdown()
    assert parser("1. First\n2. Second\n\nSome text\n\n1. First\n2. Second") == "1. First\n2. Second\n\nSome text\n\n1. First\n2. Second"
    assert parser("1. First\n2. Second\n\nSome text\n\n3. Third\n4. Fourth") == "1. First\n2. Second\n\nSome text\n\n3. Third\n4. Fourth"

def test_blockquote():
    parser = SlackMarkdown()
    assert parser("> Blockquote") == "> Blockquote"
    assert parser("> Nested\n>> Blockquote") == "> Nested\n>> Blockquote"

def test_table():
    parser = SlackMarkdown()
    markdown = """
| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
"""
    expected_output = """```
Column 1   | Column 2  
---------- | ----------
Data 1     | Data 2    
```"""
    assert parser(markdown) == expected_output

def test_table_empty_values():
    parser = SlackMarkdown()
    markdown = """
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   |          |
"""
    expected_output = """```
Column 1   | Column 2   | Column 3  
---------- | ---------- | ----------
Data 1     | Data 2     |           
```"""
    assert parser(markdown) == expected_output

def test_mentions():
    parser = SlackMarkdown()
    assert parser("@user") == "<@user>"
    assert parser("#channel") == "<#channel>"

def test_links():
    parser = SlackMarkdown()
    assert parser("[Slack](https://slack.com)") == "<https://slack.com|Slack>"
    assert parser("[Google](https://google.com)") == "<https://google.com|Google>"

def test_images():
    parser = SlackMarkdown()
    assert parser("![Alt text](https://image.url)") == "<https://image.url|Alt text>"

def test_hrules():
    parser = SlackMarkdown()
    assert parser("---") == ""
    assert parser("***") == ""
    assert parser("___") == ""

def test_emails():
    parser = SlackMarkdown()
    assert parser("someone@example.org") == "<mailto:someone@example.org|someone@example.org>"
    text = "Reach out at [info@company.com](mailto:info@company.com?subject=Hello%20World)."
    expected = "Reach out at <mailto:info@company.com?subject=Hello%20World|info@company.com>."
    assert parser(text) == expected

def test_email_link_variants():
    parser = SlackMarkdown()
    assert parser("user.name+tag@domain.co") == "<mailto:user.name+tag@domain.co|user.name+tag@domain.co>"
    md = "Email us at [Support](mailto:support@service.com)"
    result = "Email us at <mailto:support@service.com|Support>"
    assert parser(md) == result

def test_email_formatting():
    parser = SlackMarkdown()
    assert parser("admin@portal.net") == "<mailto:admin@portal.net|admin@portal.net>"
    md = "For help, write to [admin@portal.net](mailto:admin@portal.net?subject=Need%20help)."
    expected = "For help, write to <mailto:admin@portal.net?subject=Need%20help|admin@portal.net>."
    assert parser(md) == expected

def test_mailto_link_with_name():
    parser = SlackMarkdown()
    text = "Contact [The Team](mailto:team@org.io)"
    expected = "Contact <mailto:team@org.io|The Team>"
    assert parser(text) == expected

def test_multiple_email_formats():
    parser = SlackMarkdown()
    assert parser("Email: feedback@mysite.com") == "Email: <mailto:feedback@mysite.com|feedback@mysite.com>"
    text = "Click [here](mailto:feedback@mysite.com?subject=Site%20Feedback) to send us your thoughts."
    expected = "Click <mailto:feedback@mysite.com?subject=Site%20Feedback|here> to send us your thoughts."
    assert parser(text) == expected

def test_email_with_display_name():
    parser = SlackMarkdown()
    text = "Contact [Customer Support](mailto:support@domain.com?subject=Urgent)"
    expected = "Contact <mailto:support@domain.com?subject=Urgent|Customer Support>"
    assert parser(text) == expected

def test_email_as_sentence_end():
    parser = SlackMarkdown()
    text = "You can email john.doe@company.org."
    expected = "You can email <mailto:john.doe@company.org|john.doe@company.org>."
    assert parser(text) == expected

def test_markdown_with_brackets():
    parser = SlackMarkdown()
    text = "Send feedback to [email@example.com](mailto:email@example.com?subject=[Feedback])"
    expected = "Send feedback to <mailto:email@example.com?subject=[Feedback]|email@example.com>"
    assert parser(text) == expected

def test_encoded_subject():
    parser = SlackMarkdown()
    text = "Report issues: [bugs@tracker.io](mailto:bugs@tracker.io?subject=Bug%20Report%3A%20UI)"
    expected = "Report issues: <mailto:bugs@tracker.io?subject=Bug%20Report%3A%20UI|bugs@tracker.io>"
    assert parser(text) == expected

def test_various_links():
    parser = SlackMarkdown()
    text = "Ask a question at [qa@domain.com](mailto:qa@domain.com?subject=Question)"
    expected = "Ask a question at <mailto:qa@domain.com?subject=Question|qa@domain.com>"
    assert parser(text) == expected

def test_header_with_link():
    parser = SlackMarkdown()
    markdown_input1 = "# [Slack](https://slack.com)"
    expected_output1 = "*<https://slack.com|Slack>*"
    assert parser(markdown_input1) == expected_output1

    markdown_input2 = "## A link to [Google](https://google.com) here"
    expected_output2 = "*A link to <https://google.com|Google> here*"
    assert parser(markdown_input2) == expected_output2

def test_header_with_mixed_inline_formatting():
    parser = SlackMarkdown()
    markdown = "## *Styling* with `code`, ~strike~, and a [link](https://example.com)"
    expected = "*_Styling_ with `code`, ~strike~, and a <https://example.com|link>*"
    assert parser(markdown) == expected

def test_deeply_nested_lists_with_formatting():
    parser = SlackMarkdown()
    markdown = """
- Level 1 Item
  - Level 2 with **bold**
    - Level 3 with a [link](https://google.com)
    - Level 3 for @user
- Back to Level 1
"""
    expected = """
• Level 1 Item
  • Level 2 with *bold*
    • Level 3 with a <https://google.com|link>
    • Level 3 for <@user>
• Back to Level 1
""".strip()
    assert parser(markdown) == expected

def test_blockquote_containing_list_and_link():
    parser = SlackMarkdown()
    markdown = """
> Here is a quote:
> - First point with _italics_
> - Check out [this site](https://slack.com)
"""
    expected = """> Here is a quote:
> • First point with _italics_
> • Check out <https://slack.com|this site>"""
    assert parser(markdown) == expected

def test_literal_markdown_characters():
    parser = SlackMarkdown()
    assert parser("A variable name like this_is_a_variable.") == "A variable name like this_is_a_variable."

    assert parser("Calculate it with 5 * 10.") == "Calculate it with 5 * 10."

    assert parser("This is an incomplete *bold.") == "This is an incomplete *bold."