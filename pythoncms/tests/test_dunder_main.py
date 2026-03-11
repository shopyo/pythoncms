# import os
# import pytest
# from shopyo import __main__
# def test_no_args(monkeypatch, capfd):
#      monkeypatch.setattr("sys.argv", [""])
#      __main__.main()
#      captured = capfd.readouterr()
#      assert "No arguments supplied" in captured.out
# def test_arg_no_env(monkeypatch, capfd):
#      monkeypatch.setattr("sys.argv", ["testok"])
#      __main__.main()
#      captured = capfd.readouterr()
#      assert "Please use Shopyo in a virtual environment for this command" in captured.out
from click.testing import CliRunner
from pythoncms.cli import cli

def test_no_args():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "The fastest way to build CMS in Python" in result.output
