import pytermgui as ptg
import time


def macro_time(fmt: str) -> str:
    return time.strftime(fmt)

ptg.tim.define('!time', macro_time)

def main():
    with ptg.WindowManager() as wm:
        wm.layout.add_slot('Body')
        wm.add(ptg.Window("[bold]The current time is:[/]\n\n[!time 75]%c", box="EMPTY"))

if __name__ == "__main__":
    main()