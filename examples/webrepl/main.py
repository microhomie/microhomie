import settings

from homie.device import HomieDevice
from homie.micro import MPy


def main():
    homie = HomieDevice(settings)
    homie.add_node(MPy(
        webrepl_pass=getattr(
            settings, "WEBREPL_PASS", "uhomie")
        )
    )
    homie.run_forever()


if __name__ == "__main__":
    main()
