"""Example of extending PyTEdit with custom functionality"""

import sys
from pytedit import Editor, TextBuffer


class EnhancedTextBuffer(TextBuffer):
    """Enhanced text buffer with additional features"""
    
    def __init__(self):
        super().__init__()
        self.line_numbers = True  # Display line numbers by default
    
    def toggle_line_numbers(self):
        """Toggle line number display"""
        self.line_numbers = not self.line_numbers
        return self.line_numbers


class CustomEditor(Editor):
    """Custom editor with enhanced features"""
    
    def __init__(self):
        # Replace standard TextBuffer with our enhanced version
        self.buffer = EnhancedTextBuffer()
        
        # Set custom status message
        self.status_message = "CustomEditor | Ctrl-L: Toggle Line Numbers"
        
        # Initialize the rest normally
        self.bindings = self.create_key_bindings()
        
        # Set up the UI (copied from parent class to avoid calling super().__init__())
        from prompt_toolkit.buffer import Buffer
        from prompt_toolkit.layout.containers import HSplit, Window
        from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
        from prompt_toolkit.layout.layout import Layout
        from prompt_toolkit.application import Application
        
        self.text_buffer = Buffer(
            multiline=True, 
            read_only=True
        )
        
        self.layout = Layout(
            HSplit([
                Window(
                    content=BufferControl(buffer=self.text_buffer),
                    wrap_lines=True,
                ),
                Window(
                    height=1,
                    content=FormattedTextControl(self.get_status_text),
                    style="class:status"
                )
            ])
        )
        
        self.app = Application(
            layout=self.layout,
            key_bindings=self.bindings,
            full_screen=True,
            mouse_support=True
        )
        
        self.refresh_screen()
    
    def create_key_bindings(self):
        """Create key bindings with custom shortcuts"""
        kb = super().create_key_bindings()
        
        # Add custom key binding for line numbers
        @kb.add('c-l')
        def _(event):
            """Toggle line numbers"""
            line_numbers_on = self.buffer.toggle_line_numbers()
            if line_numbers_on:
                self.status_message = "Line numbers enabled"
            else:
                self.status_message = "Line numbers disabled"
            self.refresh_screen()
        
        return kb
    
    def get_status_text(self):
        """Customize status bar text"""
        status = super().get_status_text()
        if self.buffer.line_numbers:
            return status + " | Line Numbers: ON"
        return status


def main():
    """Run the custom editor"""
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    editor = CustomEditor()
    editor.run(filename)


if __name__ == "__main__":
    main()