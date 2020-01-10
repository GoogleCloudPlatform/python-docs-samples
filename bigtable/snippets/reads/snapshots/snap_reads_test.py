# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_read_simple 1'] = '''Reading data for phone#4c410523#20190501:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

'''

snapshots['test_read_row_partial 1'] = '''Reading data for phone#4c410523#20190501:
Column Family stats_summary
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

'''

snapshots['test_read_rows 1'] = '''Reading data for phone#4c410523#20190501:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

'''

snapshots['test_read_row_range 1'] = '''Reading data for phone#4c410523#20190501:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

'''

snapshots['test_read_row_ranges 1'] = '''Reading data for phone#4c410523#20190501:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

'''

snapshots['test_read_prefix 1'] = '''Reading data for phone#4c410523#20190501:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family stats_summary
\tconnected_cell: \x00\x00\x00\x00\x00\x00\x00\x01 @2019-05-01 00:00:00+00:00
\tconnected_wifi: \x00\x00\x00\x00\x00\x00\x00\x00 @2019-05-01 00:00:00+00:00
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

'''

snapshots['test_read_filter 1'] = '''Reading data for phone#4c410523#20190501:
Column Family stats_summary
\tos_build: PQ2A.190405.003 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190502:
Column Family stats_summary
\tos_build: PQ2A.190405.004 @2019-05-01 00:00:00+00:00

Reading data for phone#4c410523#20190505:
Column Family stats_summary
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190501:
Column Family stats_summary
\tos_build: PQ2A.190401.002 @2019-05-01 00:00:00+00:00

Reading data for phone#5c10102#20190502:
Column Family stats_summary
\tos_build: PQ2A.190406.000 @2019-05-01 00:00:00+00:00

'''
