# Default list of files to be proccessed.
@default_files = ('source.tex');

# Use lualatex
$pdflatex = 'lualatex --shell-escape --synctex=1 %O %S';

# Always create PDFs
$pdf_mode = 1;

# Try 7 times at maximum then give up
$max_repeat = 5;

# Use Preview.app to preview generated PDFs
$pdf_previewer = 'open -a Skim';

