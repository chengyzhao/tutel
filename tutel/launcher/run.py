# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os, sys

def main():
    host_size = int(os.environ['OMPI_COMM_WORLD_SIZE'])
    host_rank = int(os.environ['OMPI_COMM_WORLD_RANK'])
    local_size = int(os.environ.get('LOCAL_SIZE', 1))

    master_addr = os.environ['MASTER_ADDR'] if host_size > 1 else 'localhost'
    master_port = int(os.environ.get('MASTER_PORT', 23232))

    cmd_args = [sys.executable, '-m', 'torch.distributed.launch', '--use_env',
        '--nproc_per_node=%d' % local_size,
        '--nnodes=%d' % host_size,
        '--node_rank=%d' % host_rank,
        '--master_addr=%s' % master_addr,
        '--master_port=%s' % master_port,
        '-m', 'tutel.launcher.execl',
    ] + sys.argv[1:]
    os.execl(cmd_args[0], *cmd_args)

if __name__ == "__main__":
    main()
