import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    more_description = f.read()

setuptools.setup(
    name="",
    version="0.0.2",
    author="__",
    author_email="__",
    description="Vrozart core components",
    more_description=more_description,
    more_description_content_type="text/markdown",
    # url="https://gitlab.com/",
    license="MIT",
    packages=["form_builder"],
    install_requires=open('requirements.txt').readlines()
)