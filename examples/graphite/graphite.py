import logging
from contextfree.contextfree import *

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


@register_rule(1)
def trunk():
    with scale(0.5):
        with color(hue=0.001):
            branch()

# rule branch { branch {r 30  } }
# rule branch 0.01 { line {} }

# rule line {300 * [r .1 x 2] dot {} }

# rule dot { dot {y .1  }  }
# rule dot { 
  # trail { r 90 } 
  # trail{} }
# rule dot 0.002 {line {r 90 h 0 }  }
# rule dot 0.002 {branch {r 90 h 30}  }

# rule trail { 200    * [y 2 a -0.02] grain {a -.1} }

# rule grain { gr {} }

# rule gr { gr { y 0} }
# rule gr { gr { x 1 } }
# rule gr { gr { y -0} }
# rule gr { gr { x -1}  } 
# rule gr {SQUARE {}}

def main():
    init(canvas_size=(600, 600), background_color="#e5d5ac", face_color="#0a0707", max_depth=120)
    trunk()
    write_to_png("/tmp/trunk.png")


if __name__ == "__main__":
    main()
