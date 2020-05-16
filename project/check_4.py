from docker import APIClient


class Check_4_1:

    def evaluate_container(container):
        inspection = APIClient().inspect_container(container.name)
        user = (inspection.get("Config").get("User"))
        # print(container.exec_run("/bin/cat /proc/1/status | grep Uid | awk '{print $3}'"))
        if user == "root":
            return 'KO'
        elif user == "":
            return 'KO'
        else:
            return 'OK'

