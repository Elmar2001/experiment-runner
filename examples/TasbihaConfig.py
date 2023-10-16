from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ExtendedTyping.Typing import SupportsStr
from ProgressManager.Output.OutputProcedure import OutputProcedure as output
import paramiko
import subprocess

from typing import Dict, List, Any, Optional
from pathlib import Path
from os.path import dirname, realpath
import sys
import time
class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    # ================================ USER SPECIFIC CONFIG ================================
    """The name of the experiment."""
    name:                       str             = "new_runner_experiment"

    """The path in which Experiment Runner will create a folder with the name `self.name`, in order to store the
    results from this experiment. (Path does not need to exist - it will be created if necessary.)
    Output path defaults to the config file's path, inside the folder 'experiments'"""
    results_output_path:        Path            = ROOT_DIR / 'experiments'

    """Experiment operation type. Unless you manually want to initiate each run, use `OperationType.AUTO`."""
    operation_type:             OperationType   = OperationType.AUTO

    """The time Experiment Runner will wait after a run completes.
    This can be essential to accommodate for cooldown periods on some systems."""
    time_between_runs_in_ms:    int             = 1000
    experimentCount: int = 1

    # Dynamic configurations can be one-time satisfied here before the program takes the config as-is
    # e.g. Setting some variable based on some criteria
    # def __init__(self, governor, workload):
    def __init__(self):

        """Executes immediately after program start, on config load"""

        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN, self.before_run),
            (RunnerEvents.START_RUN, self.start_run),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT, self.interact),
            (RunnerEvents.STOP_MEASUREMENT, self.stop_measurement),
            (RunnerEvents.STOP_RUN, self.stop_run),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT, self.after_experiment)
        ])
        self.run_table_model = None  # Initialized later
        # self.governor = governor  # Store the governor as an instance variable
        # self.workload = workload

        self.governor = "performance"  # Store the governor as an instance variable
        self.workload = "adduser"
        self.jmeter_command = None
        # ssh part
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()  # Load known host keys
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add unknown hosts


        self.configure_jmeter(self.workload)

        output.console_log("Custom config loaded")

    def configure_jmeter(self, workload):
        print("Configuring jmeter")
        """Configure JMeter for the specified workload type."""
        if workload == 'adduser':
            # self.jmeter_command = "jmeter -n -t findroute_1000_users.jmx"
            self.jmeter_command = "/Users/el/Downloads/apache-jmeter-5.6.2/bin/jmeter -n -t addUser.jmx"
            # self.jmeter_command = '/Users/el/Downloads/apache-jmeter-5.6.2/bin/jmeter -Jthreads="$customers" -t $1 -n -l addUser.jmx'

            print("Jmeter configured.")
            ## write others.

        

    def create_run_table_model(self) -> RunTableModel:
        """Create and return the run_table model here. A run_table is a List (rows) of tuples (columns),
        representing each run performed"""

        factor1 = FactorModel("Linux_Governor", ['performance', 'powersave'])
        factor2 = FactorModel("Workload", ['findroute (1000 users)', 'findroute (500 users)', 'findroute (100 users)',
                                                'buy tickets (1000 users)', 'buy tickets (500 users)', 'buy tickets (100 users)'])
        self.run_table_model = RunTableModel(
            factors=[factor1, factor2],
            exclude_variations=[
                # Define any exclusions as needed
            ],
            data_columns=['avg_cpu', 'avg_mem']
        )
        return self.run_table_model


    def before_experiment(self) -> None:
        """Perform any activity required before starting the experiment here
        Invoked only once during the lifetime of the program."""
        # new parts for ssh
        # print("Establishing ssh connection...")
        # self.ssh.connect('145.108.225.17', username='greenTeam', password='greenTea')
        # print("ssh connect successful")

        # output.console_log("Config.before_experiment() called!")
        #         ## Set linux governors and Jmeter configuration here

        # # configure Jmeter function call here:
        # self.configure_jmeter(self.workload)
        # # jmeter -n -t your_test_plan.jmx
        # # python3 TasbihaConfig.py --governor=performance --workload=adduser
        # # Set the Linux governor based on the specified governor type
        # if self.governor == "performance":
        #     # self.subprocess.run("sudo cpufreq-set -g performance", shell=True)
        #     stdin, stdout, stderr = self.ssh.exec_command("sudo cpufreq-set -g performance")
        #     print(stdout.read().decode())
        #     print("governor set to performance")

        # elif self.governor == "powersave":
        #     # self.subprocess.run("sudo cpufreq-set -g powersave", shell=True)
        #     stdin, stdout, stderr = self.ssh.exec_command("sudo cpufreq-set -g powersave")
        #     print(stdout.read().decode())
        # else:
            # Handle unsupported governors or configurations
        # self.ssh.close()

    def before_run(self) -> None:
        """Perform any activity required before starting a run.
        No context is available here as the run is not yet active (BEFORE RUN)"""
        # ## Set linux governors and Jmeter configuration here

        # # configure Jmeter function call here:
        # self.configure_jmeter(self.workload)
        # # jmeter -n -t your_test_plan.jmx
        # # python3 TasbihaConfig.py --governor=performance --workload=adduser
        # # Set the Linux governor based on the specified governor type
        # if self.governor == "performance":
        #     # self.subprocess.run("sudo cpufreq-set -g performance", shell=True)
        #     stdin, stdout, stderr = self.ssh.exec_command("sudo cpufreq-set -g performance")
        #     print(stdout.read().decode())
        #     print("governor set to performance")

        # elif self.governor == "powersave":
        #     # self.subprocess.run("sudo cpufreq-set -g powersave", shell=True)
        #     stdin, stdout, stderr = self.ssh.exec_command("sudo cpufreq-set -g powersave")
        #     print(stdout.read().decode())
        # # else:
        #     # Handle unsupported governors or configurations
        # self.ssh.close()
        output.console_log("Config.before_run() called!")

    def start_run(self, context: RunnerContext) -> None:
        """Perform any activity required for starting the run here.
        For example, starting the target system to measure.
        Activities after starting the run should also be performed here."""
        ## Two parts: run the server, then send workloads
        ## 1. Docker Run here to start the server
        ## Sleep for some time
        ## 2. send workloads: self.subprocess.run(self.jmeter_command, shell=True)
        # print("Running jmeter subprocess")
        # result = subprocess.run(self.jmeter_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print("Input:", self.jmeter_command)
        # print("Output:", result.stdout.decode('utf-8'))
        # print("Error:", result.stderr.decode('utf-8'))
        # stdin, stdout, stderr = self.ssh.exec_command("docker system prune -a")
        # print(stdout.read().decode())
        # stdin, stdout, stderr = self.ssh.exec_command("docker-compose -f docker-compose.yml up")

        output.console_log("Config.start_run() called!")

        print("Running jmeter subprocess")
        result = subprocess.Popen(self.jmeter_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Jmeter command run:", self.jmeter_command)

    def start_measurement(self, context: RunnerContext) -> None:
        """Perform any activity required for starting measurements."""
        ## Collect CPU and memory usage. docker stats command
        # stdin, stdout, stderr = self.ssh.exec_command("timeout 5s docker stats --format \"table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | awk '{print $1","$2","$3}\' > docker_usage.csv")

        output.console_log("Config.start_measurement() called!")

        print("Sleeping for 1 sec")
        time.sleep(1)
        print("Starting measurement..")
        measurementCommand = '''timeout 5s docker stats --format "table {{.Name}}\\t{{.CPUPerc}}\\t{{.MemUsage}}" | awk \'{print $1","$2","$3}\' > docker_usage'''
        measurementCommand = measurementCommand + str(experimentCount) + '.csv'
        experimentCount = experimentCount + 1
        print("EXP COUNT", experimentCount)
        # measurementCommand = "mkdir testDir"
        print(measurementCommand)
        print("Establishing ssh connection...")
        self.ssh.connect('145.108.225.17', username='greenTeam', password='greenTea')
        print("ssh connect successful")
        paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

        stdin, stdout, stderr = self.ssh.exec_command(measurementCommand)
        
        print("Measurement command sent via SSH")
        print(stdout.read().decode())
        print(stderr.read().decode())
        self.ssh.close()

    def interact(self, context: RunnerContext) -> None:
        """Perform any interaction with the running target system here, or block here until the target finishes."""
        ## ignore
        output.console_log("Config.interact() called!")

    def stop_measurement(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping measurements."""
        ## Save the resource utilization metrics in CSV. docker stats command 
        # self.subprocess.run("docker stats --format \"table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\" | awk '{print $1\",\"$2\",\"$3}' > docker_usage.csv", shell=True)
        output.console_log("Config.stop_measurement called!")

    def stop_run(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping the run.
        Activities after stopping the run should also be performed here."""
        ## clean up database. 

        output.console_log("Config.stop_run() called!")

    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, SupportsStr]]:
        """Parse and process any measurement data here.
        You can also store the raw measurement data under `context.run_dir`
        Returns a dictionary with keys `self.run_table_model.data_columns` and their values populated"""
        # Process the measurement data (adjust the data processing code)
        ## Use the generated CSV (in stop measurement function)

        output.console_log("Config.populate_run_data() called!")
        # return data
    
    def after_experiment(self) -> None:
        """Perform any activity required after stopping the experiment here
        Invoked only once during the lifetime of the program."""

        output.console_log("Config.after_experiment() called!")

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path:            Path             = None
