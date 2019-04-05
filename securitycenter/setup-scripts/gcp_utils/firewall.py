""" firewall rules utilities methods """

from contextlib import contextmanager

from .base import LOGGER, log_exception, run_command


@contextmanager
def firewall_rules(project_id, rules):
    """
    Create firewall rules that will be dropped after execution of the block.
        :param project_id: the project where firewall rules will exist
        :param rules: list of dicts with port, tag and name keys
    """
    try:
        for rule in rules:
            allow_firewall_rule(
                project_id,
                rule['port'],
                rule['tag'],
                rule['name'])

        yield
    finally:
        for rule in reversed(rules):
            delete_firewall_rule(
                project_id,
                rule['name'])


def allow_firewall_rule(project_id, port, tag, rule_name):
    """
    Allow firewall rule.
        :param project_id: the project where firewall rule will be created
        :param port: port that will be allowed the flow
        :param tag: tag
        :param rule_name: name of the rule
    """
    with log_exception():
        LOGGER.info("Adding firewall rule for port %s", port)
        cmd = [
            'gcloud', 'compute',
            '--project "{}"'.format(project_id),
            'firewall-rules', 'create "{}"'.format(rule_name),
            '--allow', 'tcp:{}'.format(port),
            '--source-ranges "0.0.0.0/0"',
            '--target-tags "{}"'.format(tag)
        ]
        run_command(cmd)


def delete_firewall_rule(project_id, rule_name):
    """
    Delete firewall rule.
        :param project_id: the project where firewall rule will be removed
        :param rule_name: 
    """
    cmd = [
        "gcloud", "compute", "firewall-rules",
        "delete", rule_name,
        '--project "{}"'.format(project_id),
        '-q'
    ]
    run_command(cmd)
