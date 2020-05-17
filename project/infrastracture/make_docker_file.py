class Make_docker_file:

    def write_docker_file(container,fixes):
        f = open('/tmp/Dockefile', mode='wt', encoding='utf-8')
        f.write("FROM" + str(container.image) + "\n")
        f.write(fixes)
        f.close()