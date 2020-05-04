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

    def fix_container(container):
        f = open('/tmp/Dockefile', mode='wt', encoding='utf-8')
        f.write("FROM" + str(container.image) + "\n")
        f.write("RUN useradd -d /home/username -m -s /bin/bash username" + "\n")
        f.write("USER username" + "\n")
        f.close()
