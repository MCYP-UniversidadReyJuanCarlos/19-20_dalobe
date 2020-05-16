
class Fix_4_1:

    def fix_container(container,fixes):
        f = open('/tmp/Dockefile', mode='wt', encoding='utf-8')
        f.write("FROM" + str(container.image) + "\n")
        f.write("RUN useradd -d /home/username -m -s /bin/bash username" + "\n")
        f.write("USER username" + "\n")
        f.close()
