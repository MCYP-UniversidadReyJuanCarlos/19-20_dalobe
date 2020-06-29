

class Make_docker_file:

    def write_docker_file_from_dynamic(container,fixes):
        image = container.image
        f = open('output/Dockerfile', mode='wt', encoding='utf-8')
        f.write("FROM " + str(image.attrs.get('RepoTags')[0]) + "\n\n")
        f.write(fixes)
        f.close()

    def write_docker_file_from_static(instructions, dockerfile_fixes):
        f = open('output/Dockerfile', mode='wt', encoding='utf-8')
        [f.write(o['content']) for o in instructions]
        [f.write(o['content']) for o in dockerfile_fixes]
        f.close()