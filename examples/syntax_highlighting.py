"""Example of adding syntax highlighting to PyTEdit"""

import sys
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from pygments.lexers import get_lexer_for_filename, Python3Lexer
from pytedit import Editor, TextBuffer


class SyntaxHighlightingEditor(Editor):
    """Editor with syntax highlighting support"""
    
    def __init__(self):
        # Initialize the text buffer
        self.buffer = TextBuffer()
        self.status_message = "Syntax Highlighting Editor | Ctrl-S: Save | Ctrl-Q: Quit"
        self.bindings = self.create_key_bindings()
        
        # Initialize UI components manually
        from prompt_toolkit.buffer import Buffer
        from prompt_toolkit.application import Application
        
        # Create a Pygments lexer based on file extension
        self.lexer = None
        
        # Create prompt_toolkit components with syntax highlighting
        self.text_buffer = Buffer(
            multiline=True,
            read_only=True
        )
        
        # Create layout with syntax highlighting
        self.layout = Layout(
            HSplit([
                # Main editing area with syntax highlighting
                Window(
                    content=BufferControl(
                        buffer=self.text_buffer,
                        lexer=PygmentsLexer(Python3Lexer)  # Default to Python
                    ),
                    wrap_lines=True,
                ),
                # Status bar
                Window(
                    height=1,
                    content=FormattedTextControl(self.get_status_text),
                    style="class:status"
                )
            ])
        )
        
        # Create the application
        self.app = Application(
            layout=self.layout,
            key_bindings=self.bindings,
            full_screen=True,
            mouse_support=True
        )
        
        # Update the display
        self.refresh_screen()
    
    def set_lexer_for_file(self, filename):
        """Set appropriate lexer based on file extension"""
        try:
            lexer = get_lexer_for_filename(filename)
            self.layout.containers[0].content.lexer = PygmentsLexer(lexer.__class__)
            return True
        except:
            # Default to Python if we can't detect
            self.layout.containers[0].content.lexer = PygmentsLexer(Python3Lexer)
            return False
    
    def run(self, filename=None):
        """Run with syntax highlighting"""
        if filename and self.buffer.load_file(filename):
            self.status_message = f"Loaded {filename}"
            self.set_lexer_for_file(filename)
        
        self.refresh_screen()
        self.app.run()


def main():
    """Run the syntax highlighting editor"""
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    editor = SyntaxHighlightingEditor()
    editor.run(filename)


if __name__ == "__main__":
    main()