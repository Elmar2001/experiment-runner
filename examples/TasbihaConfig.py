import re
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
import shlex
import pandas as pd
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
        # self.governors = ['performance', 'powersave', 'ondemand']
        # self.workloads = [
        #     'findroute (1000 users)', 'findroute (500 users)', 'findroute (100 users)',
        #     'buytickets (1000 users)', 'buytickets (500 users)', 'buytickets (100 users)'
        # ]
        # self.run_table_model = self.create_run_table_model(self.governors, self.workloads)
        self.powerjoularFileName = None
        self.dockerCsvFileName = None
        self.governor = "performance"  # Store the governor as an instance variable
        self.workload = "adduser"   # add pick randomly feature
        self.jmeter_command = None
        # ssh part
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()  # Load known host keys
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add unknown hosts



        output.console_log("Custom config loaded")

        

    def create_run_table_model(self) -> RunTableModel:
        """Create and return the run_table model here. A run_table is a List (rows) of tuples (columns),
        representing each run performed"""
        print("CREATING RUN TABLE")
        factor1 = FactorModel("Linux_Governor", ['performance', 'powersave'])
        factor2 = FactorModel("Workload", ['MakeConsignment_1000', 'MakeConsignment_500', 'MakeConsignment_100',
                                                'list_orders_1000', 'list_orders_500', 'list_orders_100'])
        # factor2 = FactorModel("Workload", ['MakeConsignment_1000','list_orders_1000', 'MakeConsignment_500',  'list_orders_500', 'MakeConsignment_100', 'list_orders_100'])
        self.run_table_model = RunTableModel(
            factors=[factor1, factor2],
            exclude_variations=[
                # Define any exclusions as needed
            ],
            data_columns=['avg_cpu', 'avg_mem', 'avg_cpu_powerjoular', 'avg_power'],
            shuffle=True,
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
        output.console_log("Config.start_run() called!")
        self.jmeter_command = "/Users/el/Downloads/apache-jmeter-5.6.2/bin/jmeter -n -t "
        workload = context.run_variation['Workload']
        location = str(context.run_dir) + '/'


        if workload == 'MakeConsignment_1000':
            self.jmeter_command = self.jmeter_command + "MakeConsignment.jmx -l " + location +  'results.jtl -Jusers=1000' 
        elif workload == 'MakeConsignment_500':
            self.jmeter_command = self.jmeter_command + "MakeConsignment.jmx -l "  + location +  'results.jtl -Jusers=500' 
        elif workload == 'MakeConsignment_100':
            self.jmeter_command = self.jmeter_command + "MakeConsignment.jmx -l "  + location +  'results.jtl -Jusers=100' 
        elif workload == 'list_orders_1000':
            self.jmeter_command = self.jmeter_command + "ListOrders.jmx -l "  + location +  'results.jtl -Jusers=1000' 
        elif workload == 'list_orders_500':
            self.jmeter_command = self.jmeter_command + "ListOrders.jmx -l "  + location + 'results.jtl -Jusers=500' 
        elif workload == 'list_orders_100':
            self.jmeter_command = self.jmeter_command + "ListOrders.jmx -l "  + location + 'results.jtl -Jusers=100'
        print("Jmeter successfully configured.")


    def start_measurement(self, context: RunnerContext) -> None:
        """Perform any activity required for starting measurements."""
        ## Collect CPU and memory usage. docker stats command

        output.console_log("Config.start_measurement() called!")


        print("Sleeping for 1 sec")
        time.sleep(1)

        print("Starting measurement..")
        contextGovernor = context.run_variation['Linux_Governor']
        contextWorkload = context.run_variation['Workload']


        measurementCommand = '''timeout 5s docker stats --no-stream --format "table {{.Name}}\\t{{.CPUPerc}}\\t{{.MemUsage}}" | tail -n +2 | awk '{print $1","$2","$3}' >> '''
        self.dockerCsvFileName = "docker_usage" + "_" + contextGovernor + "_" + contextWorkload + '.csv'
        measurementCommand = measurementCommand + self.dockerCsvFileName

        print(measurementCommand)
        print("Establishing ssh connection...")
        self.ssh.connect('145.108.225.17', username='greenTeam', password='greenTea')
        print("ssh connect successful")
        # paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)


        if contextGovernor == 'performance':
            governorCommand = 'echo greenTea | sudo -S cpufreq-set -g performance'
        elif contextGovernor == 'powersave':
            governorCommand = 'echo greenTea | sudo -S cpufreq-set -g powersave'

        stdinG, stdoutG, stderrG = self.ssh.exec_command(governorCommand)
        print("Powerjoular outputs:")
        print(stdoutG.read().decode())
        print(stderrG.read().decode())

        print("Set linux governor to", contextGovernor)

        print("Running jmeter subprocess")
        result = subprocess.Popen(self.jmeter_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Jmeter command run:", self.jmeter_command)

        print("Starting Powerjoular")
        profiler_cmd = 'echo greenTea | sudo -S timeout 5s powerjoular -l -f '
        self.powerjoularFileName = "powerjoular" + "_" + contextGovernor + "_" + contextWorkload + '.csv'
        profiler_cmd = profiler_cmd + self.powerjoularFileName
        print(profiler_cmd)
        # time.sleep(1) # allow the process to run a little before measuring

        stdinP, stdoutP, stderrP = self.ssh.exec_command(profiler_cmd)
        print("Started Powerjoular:", profiler_cmd)

        print("Sending measurement command...")
        stdinD, stdoutD, stderrD = self.ssh.exec_command(measurementCommand)
        print("Powerjoular outputs:")
        print(stdoutP.read().decode())
        print(stderrP.read().decode())
        print("===================")
        print("Docker measurement outputs:")
        print(stdoutD.read().decode())
        print(stderrD.read().decode())
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
        try:
            # Connect to the remote server
            self.ssh.connect('145.108.225.17', username='greenTeam', password='greenTea')
            print("SSH SUCCESS AGAIN")
            # Create an SFTP client
            sftp = self.ssh.open_sftp()

            # Download the file

            sftp.get("/home/greenTeam/" + self.dockerCsvFileName, context.run_dir / 'docker.csv')
            # time.sleep(0.5)
            sftp.get("/home/greenTeam/" + self.powerjoularFileName, context.run_dir / 'powerjoular.csv')

            print(f"File '{self.dockerCsvFileName}' downloaded successfully to", context.run_dir)
            print(f"File '{self.powerjoularFileName}' downloaded successfully to", context.run_dir)

        finally:
            # Close the SFTP session and SSH connection
            sftp.close()
            self.ssh.close()

    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, SupportsStr]]:
        """Parse and process any measurement data here.
        You can also store the raw measurement data under `context.run_dir`
        Returns a dictionary with keys `self.run_table_model.data_columns` and their values populated"""
        # Process the measurement data (adjust the data processing code)
        ## Use the generated CSV (in stop measurement function)
        output.console_log("Config.populate_run_data() called!")
        # Read the CSV file into a DataFrame
        print("tryna read", context.run_dir / 'docker.csv')

        # df = pd.read_csv(context.run_dir / 'docker.csv')
        # print("FILE READ SUCCESSFULLY")
        # # print(df[1])
        # # Remove the '%' character from the values in the second column and convert them to floats
        # df.iloc[:, 1] = df.iloc[:, 1].apply(lambda x: float(x.rstrip('%')))
        # print("RSTRIP DONE")

        # # Calculate the average of the second column
        # avg_cpu = df.iloc[:, 1].mean()
        # df.iloc[:, 2] = df.iloc[:, 2].apply(lambda x: float(re.findall(r'\d+\.\d+', x)[0]))
        # # Calculate the average of the third column
        # avg_mem = df.iloc[:, 1].mean()

        import csv

        values = []
        valuesMEM = []

        with open(context.run_dir / 'docker.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[2] == '0B':
                    continue

                value = float(row[1].strip('%'))
                # print("APPENDING VALUE", value)
                values.append(value)

                valueMEM = row[2].split('MiB')[0]
                valueMEM = float(valueMEM) 
                # print("APPENDING VALUEMEM", valueMEM)

                valuesMEM.append(valueMEM)

        avg_cpu = sum(values) / len(values)
        avg_cpu = round(avg_cpu, 3)

        avg_mem = sum(valuesMEM) / len(valuesMEM) 
        avg_mem = round(avg_mem, 3)

        # ========= powerjoular ==========

        data = pd.read_csv(context.run_dir / 'powerjoular.csv')
        avg_cpu_powerjoular = data['CPU Utilization'].mean()
        avg_cpu_powerjoular = round(avg_cpu_powerjoular, 3)

        avg_power = data['Total Power'].mean()
        avg_power = round(avg_power, 3)

        run_data = {
            
            'avg_cpu': avg_cpu,
            'avg_mem': avg_mem,
            'avg_cpu_powerjoular': avg_cpu_powerjoular,
            'avg_power': avg_power
        }

        return run_data
        # return data
    
    def after_experiment(self) -> None:
        """Perform any activity required after stopping the experiment here
        Invoked only once during the lifetime of the program."""

        output.console_log("Config.after_experiment() called!")

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path:            Path             = None
