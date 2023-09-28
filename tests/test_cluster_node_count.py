from click.testing import CliRunner

from check_patroni.cli import main


def test_cluster_node_count_ok(
    runner: CliRunner, fake_restapi, use_old_replica_state: bool
) -> None:
    fake_restapi("cluster_node_count_ok")
    result = runner.invoke(
        main, ["-e", "https://10.20.199.3:8008", "cluster_node_count"]
    )
    assert result.exit_code == 0
    if use_old_replica_state:
        assert (
            result.output
            == "CLUSTERNODECOUNT OK - members is 3 | healthy_members=3 members=3 role_leader=1 role_replica=2 state_running=3\n"
        )
    else:
        assert (
            result.output
            == "CLUSTERNODECOUNT OK - members is 3 | healthy_members=3 members=3 role_leader=1 role_replica=2 state_running=1 state_streaming=2\n"
        )


def test_cluster_node_count_ok_with_thresholds(
    runner: CliRunner, fake_restapi, use_old_replica_state: bool
) -> None:
    fake_restapi("cluster_node_count_ok")
    result = runner.invoke(
        main,
        [
            "-e",
            "https://10.20.199.3:8008",
            "cluster_node_count",
            "--warning",
            "@0:1",
            "--critical",
            "@2",
            "--healthy-warning",
            "@2",
            "--healthy-critical",
            "@0:1",
        ],
    )
    assert result.exit_code == 0
    if use_old_replica_state:
        assert (
            result.output
            == "CLUSTERNODECOUNT OK - members is 3 | healthy_members=3;@2;@1 members=3;@1;@2 role_leader=1 role_replica=2 state_running=3\n"
        )
    else:
        assert (
            result.output
            == "CLUSTERNODECOUNT OK - members is 3 | healthy_members=3;@2;@1 members=3;@1;@2 role_leader=1 role_replica=2 state_running=1 state_streaming=2\n"
        )


def test_cluster_node_count_healthy_warning(
    runner: CliRunner, fake_restapi, use_old_replica_state: bool
) -> None:
    fake_restapi("cluster_node_count_healthy_warning")
    result = runner.invoke(
        main,
        [
            "-e",
            "https://10.20.199.3:8008",
            "cluster_node_count",
            "--healthy-warning",
            "@2",
            "--healthy-critical",
            "@0:1",
        ],
    )
    assert result.exit_code == 1
    if use_old_replica_state:
        assert (
            result.output
            == "CLUSTERNODECOUNT WARNING - healthy_members is 2 (outside range @0:2) | healthy_members=2;@2;@1 members=2 role_leader=1 role_replica=1 state_running=2\n"
        )
    else:
        assert (
            result.output
            == "CLUSTERNODECOUNT WARNING - healthy_members is 2 (outside range @0:2) | healthy_members=2;@2;@1 members=2 role_leader=1 role_replica=1 state_running=1 state_streaming=1\n"
        )


def test_cluster_node_count_healthy_critical(runner: CliRunner, fake_restapi) -> None:
    fake_restapi("cluster_node_count_healthy_critical")
    result = runner.invoke(
        main,
        [
            "-e",
            "https://10.20.199.3:8008",
            "cluster_node_count",
            "--healthy-warning",
            "@2",
            "--healthy-critical",
            "@0:1",
        ],
    )
    assert result.exit_code == 2
    assert (
        result.output
        == "CLUSTERNODECOUNT CRITICAL - healthy_members is 1 (outside range @0:1) | healthy_members=1;@2;@1 members=3 role_leader=1 role_replica=2 state_running=1 state_start_failed=2\n"
    )


def test_cluster_node_count_warning(
    runner: CliRunner, fake_restapi, use_old_replica_state: bool
) -> None:
    fake_restapi("cluster_node_count_warning")
    result = runner.invoke(
        main,
        [
            "-e",
            "https://10.20.199.3:8008",
            "cluster_node_count",
            "--warning",
            "@2",
            "--critical",
            "@0:1",
        ],
    )
    assert result.exit_code == 1
    if use_old_replica_state:
        assert (
            result.stdout
            == "CLUSTERNODECOUNT WARNING - members is 2 (outside range @0:2) | healthy_members=2 members=2;@2;@1 role_leader=1 role_replica=1 state_running=2\n"
        )
    else:
        assert (
            result.stdout
            == "CLUSTERNODECOUNT WARNING - members is 2 (outside range @0:2) | healthy_members=2 members=2;@2;@1 role_leader=1 role_replica=1 state_running=1 state_streaming=1\n"
        )


def test_cluster_node_count_critical(runner: CliRunner, fake_restapi) -> None:
    fake_restapi("cluster_node_count_critical")
    result = runner.invoke(
        main,
        [
            "-e",
            "https://10.20.199.3:8008",
            "cluster_node_count",
            "--warning",
            "@2",
            "--critical",
            "@0:1",
        ],
    )
    assert result.exit_code == 2
    assert (
        result.stdout
        == "CLUSTERNODECOUNT CRITICAL - members is 1 (outside range @0:1) | healthy_members=1 members=1;@2;@1 role_leader=1 state_running=1\n"
    )
