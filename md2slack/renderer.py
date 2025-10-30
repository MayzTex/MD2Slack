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
            token_type = token['type']
            
            if token_type in ['UNORDERED_LIST', 'LETTERED_LIST']:
                list_counters.pop(indent_level, None)
            elif token_type not in [
                'NUMBERED_LIST', 'PARAGRAPH', 'PARAGRAPH_BREAK'
            ]:
                list_counters.pop(indent_level, None)

            if token_type == 'HRULE':
                output.append("\n")
            elif token_type == 'PARAGRAPH':
                output.append(f"{indent_spaces}{token['value']}")
            elif token_type == 'PARAGRAPH_BREAK':
                output.append("\n")
            elif token_type == 'CODE_BLOCK':
                output.append(f"{token['value']}")
            elif token_type == 'TABLE':
                table_text = self._format_table(token['value'])
                output.append(f"{table_text}\n")
            elif token_type == 'BLOCK_QUOTE':
                quote_prefix = '>' * token['level']
                value = token['value']
                list_match = re.match(r'^\s*([-*])\s+(.*)', value)
                if list_match:
                    list_content = list_match.group(2)
                    output.append(f"{quote_prefix} • {list_content}")
                else:
                    output.append(f"{quote_prefix} {indent_spaces}{value}")
            elif token_type == 'HEADER':
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
            
            elif token_type == 'NUMBERED_LIST':
                number = token['number']
                
                current_count = list_counters.get(indent_level, 1)
                bullet = ""

                if number == 1:
                    list_counters[indent_level] = 2
                    bullet = "1."
                elif number == current_count:
                    list_counters[indent_level] = number + 1
                    bullet = f"{number}."
                else:
                    list_counters[indent_level] = number + 1
                    bullet = f"{number}."
                
                output.append(f"{indent_spaces}{bullet} {token['value']}")

            elif token_type == 'LETTERED_LIST':
                bullet = f"{token['bullet']}"
                output.append(f"{indent_spaces}{bullet} {token['value']}")
            
            elif token_type == 'UNORDERED_LIST':
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
        rows_raw = [row.strip('|').split('|') for row in table_md.strip().split('\n') if row.strip()]
        
        # Trim each cell
        rows = [[cell.strip() for cell in row] for row in rows_raw]
        
        # Handle empty tables
        if not rows:
            return "```\n```"
            
        # 1. Find max number of columns
        max_cols = max(len(row) for row in rows)
        
        # 2. Pad all rows to have the same number of columns
        padded_rows = [row + [''] * (max_cols - len(row)) for row in rows]

        # Calculate max column width using the *padded* rows
        col_widths = [max(len(cell) for cell in column) for column in zip(*padded_rows)]

        # Format rows with properly spaced columns
        formatted_rows = []
        for row in padded_rows: # Use padded_rows here
            # We can be sure col_widths[idx] is safe because row and col_widths are based on max_cols
            formatted_row = " | ".join(cell.ljust(col_widths[idx]) for idx, cell in enumerate(row))
            formatted_rows.append(formatted_row)

        return "```\n" + "\n".join(formatted_rows) + "\n```"