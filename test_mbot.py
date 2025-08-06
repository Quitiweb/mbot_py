import time

if __name__ == '__main__':
    from mbot_py.lib.mBot import mBot

    print("Iniciando test...")
    mbot = mBot()

    print("Forward...")
    mbot.doMove(100, 100)
    time.sleep(2)

    print("Stop...")
    mbot.doMove(0, 0)
    time.sleep(1)

    print("Backward...")
    mbot.doMove(-100, -100)
    time.sleep(2)

    print("Stop...")
    mbot.doMove(0, 0)
    time.sleep(1)

    print("Test completado")
    mbot.close()
