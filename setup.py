from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="tfm",
    version="0.1",
    packages=find_packages(),
    dependency_links=[
        "https://download.pytorch.org/whl/cu124/torch-2.5.0+cu124-cp310-cp310-win_amd64.whl",
        "https://download.pytorch.org/whl/cu124/torchaudio-2.4.0+cu124-cp310-cp310-win_amd64.whl",
        "https://download.pytorch.org/whl/cu124/torchvision-0.19.0+cu124-cp310-cp310-win_amd64.whl",
        "https://download.pytorch.org/whl/cu124"],
    install_requires=requirements,

    entry_points={
        "console_scripts": [
        ]
    },
    include_package_data=True,
    description="Descripción del proyecto",
    author="scabbed_wings",
    author_email="scabbed.wings.demon@gmail.com",
    url="https://github.com/scabbed-wings/proyecto-tfm",
)
