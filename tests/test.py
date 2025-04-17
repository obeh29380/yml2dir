import os
import shutil

from y2d import converter

current_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs('.output', exist_ok=True)
converter.apply(os.path.join(current_dir, 'test1.yaml'))
shutil.rmtree('.output')
