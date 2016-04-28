# Copyright 2016 - Wipro Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" This module creates the initial database and tables required for galaxia"""
# https://github.com/bosun-monitor/bosun/blob/master/cmd/scollector/collectors/cadvisor.go - This has tbe
# detailed description on each of the metrics types
# https://github.com/google/cadvisor/blob/master/info/v1/container.go
# https://github.com/google/cadvisor/blob/master/metrics/prometheus.go
# WARNING: DO NOT EDIT THIS FILE

from sqlalchemy import create_engine
import sys
from optparse import OptionParser


def main():
    parser = OptionParser()
    parser.add_option("--host", help="Database provider host address", default="localhost")
    parser.add_option("--type", help="Database type valid values are mysql", default="mysql")
    parser.add_option("--username", help="Username to login to database")
    parser.add_option("--password", help="Password to login to database")

    (options, args) = parser.parse_args()

    db_url = options.type+"://"+options.username+":"+options.password+"@"+options.host
    galaxia_db_url = db_url + "/galaxia"

    print "Connecting to "+options.type + " database@"+ options.host
    engine = create_engine(db_url)
    conn = engine.connect()

    print "Creating database galaxia"
    conn.execute("CREATE DATABASE galaxia")

    print "Connecting to galaxia database"
    engine = create_engine(galaxia_db_url)
    conn = engine.connect()

    print "Creating Dashboard Table in galaxia database"
    conn.execute("CREATE TABLE DASHBOARD(NAME VARCHAR(20),\
                 CONTAINERS VARCHAR(500), METRICS VARCHAR(50),\
                 DASHBOARD_URL VARCHAR(50), STATUS VARCHAR(15),\
                 DATE_CREATED DATETIME, DATE_UPDATED DATETIME,\
                 PRIMARY KEY(NAME))")

    print "Creating Metrics Table in galaxia database"
    conn.execute("CREATE TABLE METRICS(METRICS_NAME VARCHAR(50),\
                 PROMETHEUS_NAME VARCHAR(100), DESCRIPTION VARCHAR(200),\
                 TYPE VARCHAR(20))")

    print "Creating OPENSTACK_TOKEN Table in galaxia database"
    conn.execute("CREATE TABLE OPENSTACK_TOKEN(ID VARCHAR(5), TOKEN VARCHAR(50)\
                 )")

    print "Creating MEXPORTER table in galaxia database"
    conn.execute("CREATE TABLE MEXPORTER(EXPORTER_NAME VARCHAR(50), "
                 "EXPORTER_ID VARCHAR(99), PRIMARY KEY(EXPORTER_NAME))")

    print "Populating OPENSTACK_TOKEN table with data"
    conn.execute("INSERT INTO OPENSTACK_TOKEN VALUES('one', 'dummy_token')")

    print "Populating Metrics Table with data"

    # INSERTING CPU STATS FOR CONTAINERS

    conn.execute("INSERT INTO METRICS VALUES('CPU_BY_CORES',\
                 'container_cpu_usage_seconds_total',\
                 'CPU usage by each core', 'container')")

    conn.execute("INSERT INTO METRICS VALUES('CPU_USAGE_TOTAL',\
                 'container_cpu_system_seconds_total',\
                 'Net CPU for all the cores', 'container')")

    # INSERTING MEMORY STATS FOR CONTAINERS

    conn.execute("INSERT INTO METRICS VALUES('MEMORY_USAGE_TOTAL',\
                 'container_memory_usage_bytes',\
                 'This includes all the memory regardless of when it was\
                 accessed', 'container')")

    conn.execute("INSERT INTO METRICS VALUES('RECENTLY_ACCESSED_MEMORY',\
                 'container_memory_working_set_bytes',\
                 'This includes recently accessed memory', 'container')")

    conn.execute("INSERT INTO METRICS VALUES('MEMORY_ALLOCATION_FAILURES',\
                 'container_memory_failures_total',\
                 'Count of all memory allocation failure', 'container')")

    # INSERTING NETWORK STATS FOR CONTAINERS

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_BYTES_RECEIVED',\
                 'container_network_receive_bytes_total',\
                 'Cumulative count of bytes received', 'container')")

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_RECEIVE_ERRORS',\
                 'container_network_receive_errors_total',\
                 'Cumulative count of errors encountered while receiving',\
                 'container')")

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_RECEIVE_PACKETS_DROPPED',\
                 'container_network_receive_packets_dropped_total',\
                 'Cumulative count of packets dropped while receiving',\
                 'container')")

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_RECEIVE_PACKETS',\
                 'container_network_receive_packets_total',\
                 'Cumulative count of packets received', 'container')")

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_BYTES_TRANSMIT',\
                 'container_network_transmit_bytes_total',\
                 'Cumulative count of bytes transmitted', 'container')")

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_TRANSMIT_PACKETS',\
                 'container_network_transmit_packets_total',\
                 'Cumulative count of packets transmitted', 'container')")

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_TRANSMIT_DROPPED_PACKETS',\
                 'container_network_transmit_packets_dropped_total',\
                 'Cumulative count of packets dropped while transmitting',\
                 'container')")

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_TRANSMIT,NETWORK_ERRORS',\
                 'container_network_transmit_errors_total',\
                 'Cumulative count of network errors encountered while\
                 transmitting', 'container')")

    # Inserting File System Stats  FOR CONTAINERS

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_FS_CONSUMED_BYTES',\
                 'container_fs_usage_bytes',\
                 'Number of bytes that are consumed by the container on this\
                 filesystem', 'container')")

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_FS_READ_BYTES',\
                 'container_fs_reads_total',\
                 'Cumulative count of reads completed', 'container')")

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_FS_WRITE_BYTES',\
                 'container_fs_writes_total',\
                 'Cumulative count of writes completed', 'container')")

    conn.execute("INSERT INTO METRICS VALUES('TOTAL_CURRENT_IO',\
                 'container_fs_io_current',\
                 'Number of I/Os currently in progress', 'container')")

    # Inserting CPU stats for Nodes
    conn.execute("INSERT INTO METRICS VALUES('node_cpu','node_cpu',\
                 'cpu Seconds spent in each mode','node')")

    # Inserting Disk IO stats for Nodes
    conn.execute("INSERT INTO METRICS VALUES('node_disk_bytes_read','node_disk_bytes_read',\
                 'total number of bytes read successfully','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_disk_bytes_written','node_disk_bytes_written',\
                 'total number of bytes written successfully','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_disk_io_now','node_disk_io_now',\
                 'The number of I/Os currently in progress','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_disk_io_time_ms','node_disk_io_time_ms',\
                 'Milliseconds spent doing I/Os','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_disk_io_time_weighted','node_disk_io_time_weighted',\
                 'The weighted # of milliseconds spent doing I/Os','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_disk_read_time_ms','node_disk_read_time_ms',\
                 'The total number of reads completed successfully','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_disk_reads_merged','node_disk_reads_merged',\
                 'The number of reads merged','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_disk_sectors_read','node_disk_sectors_read',\
                 'The total number of sectors read successfully','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_disk_sectors_written','node_disk_sectors_written',\
                 'The total number of sectors written successfully','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_disk_write_time_ms','node_disk_write_time_ms',\
                 'This is the total number of milliseconds spent by all writes','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_disk_writes_completed','node_disk_writes_completed',\
                 'The total number of writes completed successfully','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_disk_writes_merged','node_disk_writes_merged',\
                 'The number of writes merged','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_filesystem_free','node_filesystem_free',\
                 'Filesystem free space in bytes','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_filesystem_size','node_filesystem_size',\
                 'Filesystem size in bytes','node')")

    # Inserting Memory stats for Nodes

    conn.execute("INSERT INTO METRICS VALUES('node_memory_Cached','node_memory_Cached',\
                 'Memory information field Cached','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_memory_Buffers','node_memory_Buffers',\
                 'Memory information field Buffers','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_memory_Active','node_memory_Active',\
                 'Memory information field Active','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_memory_Inactive','node_memory_Inactive',\
                 'Memory information field Inactive','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_memory_MemAvailable','node_memory_MemAvailable',\
                 'Memory information field MemAvailable','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_memory_MemFree','node_memory_MemFree',\
                 'Memory information field MemFree','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_memory_MemTotal','node_memory_MemTotal',\
                 'Memory information field MemTotal','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_memory_SwapFree','node_memory_SwapFree',\
                 'Memory information field SwapFree','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_memory_SwapTotal','node_memory_SwapTotal',\
                 'Memory information field SwapTotal','node')")

    # Inserting Network stats for Nodes

    conn.execute("INSERT INTO METRICS VALUES('node_network_receive_bytes','node_network_receive_bytes',\
                 'Network device statistic receive_bytes','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_network_receive_compressed','node_network_receive_compressed',\
                 'Network device statistic receive_compressed','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_network_receive_drop','node_network_receive_drop',\
                 'Network device statistic receive_drop','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_network_receive_errs','node_network_receive_errs',\
                 'Network device statistic receive_errs','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_network_receive_packets','node_network_receive_packets',\
                 'Network device statistic receive_packets','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_network_transmit_bytes','node_network_transmit_bytes',\
                 'Network device statistic transmit_bytes','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_network_transmit_compressed','node_network_transmit_compressed',\
                 'Network device statistic transmit_compressed','node')")

    conn.execute("INSERT INTO METRICS VALUES('node_network_transmit_packets','node_network_transmit_packets',\
                 'Network device statistic transmit_packets','node')")



if __name__ == '__main__':
    sys.exit(main())
