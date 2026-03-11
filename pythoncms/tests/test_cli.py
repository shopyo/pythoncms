import os
import shutil
from click.testing import CliRunner
from pythoncms.cli import cli

def test_cli_start(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ["start", "mysite"])
        assert result.exit_code == 0
        assert "mysite is ready" in result.output
        assert os.path.exists("mysite")
        assert os.path.exists("mysite/.env")
        assert os.path.exists("mysite/requirements.txt")

def test_cli_deploy(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ["deploy"])
        assert result.exit_code == 0
        assert "Deployment files generated" in result.output
        assert os.path.exists("Dockerfile")
        assert os.path.exists("docker-compose.yml")
        assert os.path.exists(".dockerignore")

def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "pythoncms, version" in result.output
