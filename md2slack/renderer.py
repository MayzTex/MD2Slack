import re


class SlackRenderer:
    """
    Renders parsed Markdown tokens into Slack-compatible output.
    """
    
    def render(self, tokens):
        """
        Converts a list of tokens into Slack-compatible Markdown.

        Args:
            tokens (list): List of parsed Markdown tokens.

        Returns:
            str: Formatted Slack-compatible text.
        """
        output = []
        list_counters = {}
        
        for token in tokens:
            indent_level = token.get('indent', 0)
            indent_spaces = " " * indent_level
            
            if token['type'] == 'HRULE':
                output.append("\n")
            elif token['type'] == 'PARAGRAPH':
                output.append(f"{indent_spaces}{token['value']}")
            elif token['type'] == 'PARAGRAPH_BREAK':
                output.append("\n")
            elif token['type'] == 'CODE_BLOCK':
                output.append(f"{token['value']}")
            elif token['type'] == 'TABLE':
                table_text = self._format_table(token['value'])
                output.append(f"{table_text}\n")
            elif token['type'] == 'BLOCK_QUOTE':
                quote_prefix = '>' * token['level']
                value = token['value']
                list_match = re.match(r'^\s*([-*])\s+(.*)', value)
                if list_match:
                    list_content = list_match.group(2)
                    output.append(f"{quote_prefix} • {list_content}")
                else:
                    output.append(f"{quote_prefix} {indent_spaces}{value}")
            elif token['type'] == 'HEADER':
                raw = token.get("raw", "")
                value = token["value"]
                if re.fullmatch(r'\*{3}(.+?)\*{3}', raw):
                    inner = re.sub(r'^\*{3}(.+?)\*{3}$', r'\1', raw)
                    output.append(f"{indent_spaces}*_{inner}_*")
                elif re.fullmatch(r'\*{2}(.+?)\*{2}', raw):
                    inner = re.sub(r'^\*{2}(.+?)\*{2}$', r'\1', raw)
                    output.append(f"{indent_spaces}*{inner}*")
                elif re.fullmatch(r'\*(.+?)\*', raw):
                    inner = re.sub(r'^\*(.+?)\*$', r'\1', raw)
                    output.append(f"{indent_spaces}*_{inner}_*")
                elif re.search(r'\*{3}(.+?)\*{3}', raw):
                    inner = re.sub(r'\*{3}(.+?)\*{3}', r'\1', raw)
                    output.append(f"{indent_spaces}*_{inner}_*")
                elif re.search(r'\*{2}(.+?)\*{2}', raw):
                    inner = re.sub(r'\*{2}(.+?)\*{2}', r'\1', raw)
                    output.append(f"{indent_spaces}*{inner}*")
                elif re.search(r'\*(.+?)\*', raw):
                    inner = re.sub(r'\*(.+?)\*', r'\1', raw)
                    output.append(f"{indent_spaces}*_{inner}_*")
                else:
                    clean = re.sub(r'\*{1,3}', '', value)
                    output.append(f"{indent_spaces}*{clean}*")
            elif token['type'] in ['UNORDERED_LIST', 'NUMBERED_LIST', 'LETTERED_LIST']:
                if token['type'] == 'NUMBERED_LIST':
                    if indent_level not in list_counters:
                        list_counters[indent_level] = 1
                    bullet = f"{list_counters[indent_level]}."
                    list_counters[indent_level] += 1
                elif token['type'] == 'LETTERED_LIST':
                    bullet = f"{token['bullet']}"
                else:
                    bullet = f"{token['bullet']}"
                output.append(f"{indent_spaces}{bullet} {token['value']}")
            else:
                output.append(f"{indent_spaces}{token['value']}")
        
        return '\n'.join(output)
    
    def _format_table(self, table_md):
        """
        Formats tables for Slack by aligning columns.

        Args:
            table_md (str): The raw Markdown table text.

        Returns:
            str: Formatted table as a Slack-compatible text block.
        """
        rows = [row.strip('|').split('|') for row in table_md.strip().split('\n') if row.strip()]
        
        # Trim each cell and calculate max column width for alignment
        rows = [[cell.strip() for cell in row] for row in rows]
        col_widths = [max(len(cell) for cell in column) for column in zip(*rows)]

        # Format rows with properly spaced columns
        formatted_rows = []
        for row in rows:
            formatted_row = " | ".join(cell.ljust(col_widths[idx]) for idx, cell in enumerate(row))
            formatted_rows.append(formatted_row)

        return "```\n" + "\n".join(formatted_rows) + "\n```"