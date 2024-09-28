from setuptools import setup, find_packages

setup(
    name="ae_classification_tool",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "pandas",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "ae-classifier=ae_classifier:main",
        ],
    },
)
