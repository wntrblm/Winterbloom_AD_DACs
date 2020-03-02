import nox


@nox.session(python="3")
def blacken(session):
    """Run black code formater."""
    session.install("black==19.3b0", "isort==4.3.21")
    files = ["noxfile.py", "winterbloom_ad_dacs"]
    session.run("black", *files)
    session.run("isort", "--recursive", *files)


@nox.session(python="3.7")
def lint(session):
    session.install("flake8==3.7.8", "black==19.3b0")
    files = ["noxfile.py", "winterbloom_ad_dacs"]
    session.run("black", "--check", *files)
    session.run("flake8", *files)
