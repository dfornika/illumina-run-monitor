# illumina-run-monitor

Watch an illumina sequencer output directory to monitor progress of sequencing runs.

# Installation

```
conda create -n illumina-run-monitor python=3
git clone https://github.com/dfornika/illumina-run-monitor.git
cd illumina-run-monitor
pip install .
```

If installing for development purposes, instead of the `pip` command above, use the 'editable' mode:

```
pip install -e .
```

# Usage

```
monitor-dir --dir /path/to/sequencer-output-dir
```