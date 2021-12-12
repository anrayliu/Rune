import os #getcwd(), chdir(), path.dirname(), isabs()
import argparse 


parser = argparse.ArgumentParser()
parser.add_argument("-ws", "--window_size", type=int, nargs=2, default=(426, 240))
parser.add_argument("-ar", "--aspect_ratio", type=int, nargs=2, default=(16, 9))
parser.add_argument("-r", "--resizable", action="store_true")
parser.add_argument("-m", "--mute", action="store_true")
parser.add_argument("-l", "--loop", action="store_true")
parser.add_argument("file", type=str)
args = parser.parse_args()

config = {"path":os.getcwd(),
          "window_size":args.window_size,
          "aspect_ratio":args.aspect_ratio,
          "resizable":args.resizable,
          "mute":args.mute,
          "loop":args.loop}
          
os.chdir(os.path.dirname(__file__))

if args.file != None:
    if os.path.isabs(args.file):
        config["path"], config["file"] = os.path.split(args.file)
    else:
        config["file"] = args.file