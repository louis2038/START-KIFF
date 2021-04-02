from cx_Freeze import setup, Executable

executables = [Executable("main.py")]

includefiles = ["asteroide_2.png",
                "asteroide_1.png",
                "avion.png",
                "base.db",
                "caprice.wav",
                "cloche.wav",
                "main.py"
                ]



options = {
    "include_files": includefiles,
}

setup(
    name="STAR-SKIFF",
    base="base.db",
    version="1",
    description="createur louis",
    options={"build_exe": options},
    executables=executables
)