"""Task Definitions"""


def task_fixup():
    """Run Formatters"""
    return {
        "actions": [
            "isort --profile=black .",
            "pyupgrade --py311-plus",
            "black .",
            "mdformat .",
            "nbqa isort --profile=black index.ipynb",
            "nbqa pyupgrade --py311-plus index.ipynb",
            "nbqa black index.ipynb",
            "nbqa --nbqa-md mdformat --wrap=100 --number index.ipynb",
        ]
    }


def task_test():
    """Run Tests"""
    return {"actions": ["pylint --recursive=y .", "nbqa pylint index.ipynb"]}
