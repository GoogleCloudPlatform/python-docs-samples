class PatchedIPython:
    @staticmethod
    def system(cmd: str) -> None:
        print(f"!{cmd}")


def get_ipython() -> PatchedIPython:
    return PatchedIPython()
