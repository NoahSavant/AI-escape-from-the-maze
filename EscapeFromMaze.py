from MazeEscape import *
from UICreateMap import *

while True:
    num_agent, real_map = EnterSize().Run()
    if not real_map:
        break;
    CentralSystem(num_agent, real_map).run()  # hệ thống chính

