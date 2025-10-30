import re

class SlackBlockGrammar:
    """
    Defines the block-level grammar for converting Markdown to Slack format.
    These regex patterns match various block-level elements such as headers,
    lists, block quotes, and tables.
    """
    # Header syntax, supporting up to 6 levels (e.g., # Header, ## Header, etc.)
    HEADER = re.compile(r'^(#{1,6})\s+(.+)', re.M)

    # Matches empty headers (e.g., # , ## , etc.)
    EMPTY_HEADER = re.compile(r'^(#{1,6})\s*$', re.M)
    
    # Matches fenced code blocks (```code```)
    CODE_BLOCK = re.compile(r'```([\s\S]+?)```', re.M)
    
    # Matches unordered lists (- item or * item)
    UNORDERED_LIST = re.compile(r'^( *)([-*])\s+(.+)', re.M)
    
    # Matches ordered (numbered) lists (1. item, 2. item, etc.)
    NUMBERED_LIST = re.compile(r'^( *)(\d+)\.\s+(.+)', re.M)
    
    # Matches lettered lists (A) item, B) item, etc.)
    LETTERED_LIST = re.compile(r'^( *)([A-Z])\)\s+(.+)', re.M)
    
    # Matches Setext-style headers (underlined headers with === or ---)
    SETEXT_HEADER = re.compile(r'^(?!#)([^\n]+)\n(=+|-+)\s*$', re.M)
    
    # Matches horizontal rules (---, ***, ___)
    HRULE = re.compile(r'^ {0,3}([-*_])(?: *\1){2,} *(?:\n+|$)', re.M)
    
    # Matches paragraph breaks (empty lines separating paragraphs)
    PARAGRAPH_BREAK = re.compile(r'^\s*\n', re.M)
    
    # Matches paragraphs (avoiding headers, lists, quotes, tables, etc.)
    PARAGRAPH = re.compile(r'^(?!#|\s*[-*>]|```|\||\d+\.|[A-Z]\)|\s*$)(.+)', re.M)
    
    # Matches block quotes (> quoted text)
    BLOCK_QUOTE = re.compile(r'^( *>+)\s*(.*)', re.M)
    
    # Matches tables (rows with pipes "|")
    TABLE = re.compile(r'^.*\|.*\|.*$', re.M)


class SlackInlineGrammar:
    """
    Defines the inline-level grammar for converting Markdown to Slack format.
    These regex patterns match inline elements such as bold, italics, strikethrough,
    inline code, links, images, and mentions.
    """
    # Matches bold and italic text (***bold italic***)
    BOLD_ITALIC = re.compile(r'(\*\*\*|___)(.+?)\1')
    
    # Matches bold text (**bold** or __bold__)
    BOLD = re.compile(r'(\*\*|__)(.+?)\1')
    
    # Matches italic text (*italic* or _italic_)
    ITALIC = re.compile(
        r'(?<!\*)\*(?!\*)(\S.+?\S)\*(?!\*)|(?<!_)_(?!_)(\S.+?\S)_(?!_)'
    )
    
    # Matches strikethrough text (~strikethrough~)
    STRIKETHROUGH = re.compile(r'~(.+?)~')
    
    # Matches inline code (`code`)
    INLINE_CODE = re.compile(r'`(.+?)`')
    
    # Matches Markdown-style links ([text](http://example.com))
    LINK = re.compile(r'\[(.+?)\]\((https?://[^\)]+)\)')
    
    # Matches Markdown-style images (![alt text](image_url))
    IMAGE = re.compile(r'!\[(.*?)\]\((.+?)(?:\s".*?")?\)')
    
    # Matches Slack user mentions (<@USERID>)
    MENTION_USER = re.compile(r'(?<![\w<])@([a-zA-Z0-9_]+)\b|<@([A-Z0-9]+)>')
    
    # Matches Slack channel mentions (<#CHANNELID>)
    MENTION_CHANNEL = re.compile(r'(#[a-zA-Z0-9_]+|<#([A-Z0-9]+)>)')
    
    # Matches line breaks (two spaces followed by a newline)
    LINEBREAK = re.compile(r'  \n')

    # Matches raw email addresses (0rE3D@example.com, etc.)
    RAW_EMAIL = re.compile(
        r'(?<![\w<@])'  # Ensure the email is not preceded by a word character, '<', or '@'
        r'(?<!mailto:)'  # Ensure the email is not preceded by 'mailto:'
        r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'  # Match the email address
        r'(?![\w>])'  # Ensure the email is not followed by a word character or '>'
        r'(?!\?subject=)'  # Exclude emails that are part of a mailto link with a subject
    )

    # Matches email links ([email](mailto:0rE3D@example.com))
    MAILTO_LINK = re.compile(r'\[([^\]]+?)\]\((mailto:[^)]+?)\)')
