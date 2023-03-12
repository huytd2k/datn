import graphviz
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter
from graphviz.backend import run as run_dot


class GraphVizWidget(QWidget):
    def __init__(self, dotcode: graphviz.Digraph):
        super().__init__()
        self.dotcode = dotcode
        self.image = None

    def render(self):
        self.image = None
        svg_string = self.dotcode.create_svg(prog='dot')

        options = ['-Tpng', '-Kdot']
        data = self.dotcode.encode("UTF-8")
        try:
            result = run_dot(options=options, stdin=data)
            if result.returncode == 0:
                self.image = QPixmap()
                self.image.loadFromData(result.stdout)
        except:
            pass

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.image:
            painter.drawPixmap(0, 0, self.image)


# Your original Red-Black tree code
rb_tree_data = [('root', 'A'), ('A', 'B'), ('A', 'C'), ('C', 'D')]
rb_tree_edges = [(f'{src}', f'{dst}') for src, dst in rb_tree_data]

# Create a Graphviz Digraph object
dot = graphviz.Digraph()
for edge in rb_tree_edges:
    dot.edge(*edge)

dot_html = dot.pipe().decode('utf-8')

app = QApplication([])
widget = GraphVizWidget(dot_html)

# Render the widget
widget.render()

layout = QVBoxLayout()
layout.addWidget(widget)
# Set the layout of the main window
window = QWidget()
window.setLayout(layout)

# Show the main window.
window.show()
app.exec_()

