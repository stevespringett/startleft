import pytest

from startleft.startleft._version.version_scheme import choose_strategy_by_branch, guess_startleft_semver, DEFAULT_VERSION
from .version_mocks import *


class TestVersionScheme:
    # To simplify the methods naming, we use the following acronyms:
    # - RTP (or rtp) stands for Release Testing Period.
    # - RP (or rtp) stands for Release Period.

    @pytest.mark.parametrize('branch,expected_strategy', [
        ('main', '_tag_version_strategy'),
        ('hotfix/XXX-000', '_patch_version_dev_commit_strategy'),
        ('release/1.5.0', '_tag_version_strategy'),
        ('bugfix/XXX-000', '_tag_version_dev_commit_strategy'),
        ('dev', '_minor_version_dev_commit_strategy'),
        ('feature/XXX-000', '_minor_version_dev_commit_strategy'),
        ('UNKNOWN_BRANCH_PATTERN', '_minor_version_dev_commit_strategy'),
    ])
    def test_strategy_by_branch(self, branch, expected_strategy):
        # GIVEN some branch
        # WHEN choose_strategy_by_branch is called
        strategy_fn = choose_strategy_by_branch(branch)

        # THEN the right strategy is chosen
        assert strategy_fn.__name__ == expected_strategy

    @pytest.mark.parametrize('scm_version,expected_version', [
        # MAIN
        (MAIN_NO_HOTFIX_VERSION, '1.5.0'),
        (MAIN_HOTFIX_VERSION, '1.5.1'),
        # HOTFIX
        (HOTFIX_VERSION, '1.5.1.dev18'),
        # RELEASE
        (RELEASE_VERSION_NO_BUGFIX, '1.6.0rc1'),
        (RELEASE_VERSION_BUGFIX, '1.6.0rc1'),
        # BUGFIX
        (BUGFIX_VERSION, '1.6.0rc1.dev1'),
        # DEV
        (DEV_RTP_VERSION, '1.7.0.dev19'),
        (DEV_RTP_NO_DISTANCE_VERSION, '1.7.0'),
        (DEV_RP_VERSION, '1.7.0.dev3'),
        (DEV_RP_HOTFIX_VERSION, '1.7.0.dev3'),
        # FEATURE
        (FEATURE_RTP_VERSION, '1.7.0.dev3'),
        (FEATURE_RP_VERSION, '1.7.0.dev4'),
        (FEATURE_RP_HOTFIX_VERSION, '1.7.0.dev14'),
        # FREE BRANCH
        (FREE_BRANCH_RTP_VERSION, '1.7.0.dev7'),
        (FREE_BRANCH_RP_VERSION, '1.7.0.dev2'),
        (FREE_BRANCH_RP_HOTFIX_VERSION, '1.7.0.dev1'),
    ], ids=[
            # MAIN
            'test_main_no_hotfix_version',
            'test_main_hotfix_version',
            # HOTFIX
            'test_hotfix_version',
            # RELEASE
            'test_release_version_no_bugfix',
            'test_release_version_bugfix',
            # BUGFIX
            'test_bugfix_version',
            # DEV
            'test_dev_rtp_version',
            'test_dev_rtp_no_distance_version',
            'test_dev_rp_version',
            'test_dev_rp_hotfix_version',
            # FEATURE
            'test_feature_rtp_version',
            'test_feature_rp_version',
            'test_feature_rp_hotfix_version',
            # FREE BRANCH
            'test_free_branch_rtp_version',
            'test_free_branch_rp_version',
            'test_free_branch_rp_hotfix_version'])
    def test_main(self, scm_version, expected_version):
        # GIVEN a ScmVersion mock
        # WHEN guess_startleft_semver is called
        version = guess_startleft_semver(scm_version)

        # THEN the expected version is returned
        assert version == expected_version

    def test_error_calculating_version(self):
        # GIVEN some invalid version
        version = Mock(branch= 'dev', tag='invalid_version')

        # WHEN guess_startleft_semver_suffix is called
        version = guess_startleft_semver(version)

        # THEN no local part is returned
        assert version == DEFAULT_VERSION
